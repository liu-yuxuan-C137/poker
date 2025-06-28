import sys
import json
import struct
import socket
import random
import math
from collections import Counter

server_ip = "127.0.0.1"                 # 德州扑克平台地址
server_port = 2333                      # 德州扑克平台开放端口

# 命令行参数将在main函数中解析
room_number = None
name = None
game_number = None


class PokerAgent:
    """
    智能德州扑克AI智能体
    基于手牌强度评估、位置策略、对手建模等多维度决策
    """

    def __init__(self):
        # 基础参数
        self.aggression_factor = 0.3  # 激进程度
        self.bluff_frequency = 0.15   # 诈唬频率
        self.tight_factor = 0.6       # 紧凶程度

        # 对手建模
        self.opponent_stats = {}      # 对手统计信息
        self.game_history = []        # 游戏历史

        # 位置权重 (按钮位置为最佳)
        self.position_weights = {
            0: 0.8,  # 小盲注
            1: 0.9,  # 大盲注/其他位置
        }

    def evaluate_hand_strength(self, hole_cards, public_cards):
        """
        评估手牌强度
        返回0-1之间的强度值
        """
        if not hole_cards or len(hole_cards) != 2:
            return 0.5

        all_cards = hole_cards + public_cards
        strength = 0.5  # 基础强度

        # 解析牌面
        ranks = [self._card_rank(card) for card in all_cards]
        suits = [card[1] if len(card) > 1 else 'S' for card in all_cards]

        # 手牌评估
        hole_ranks = [self._card_rank(card) for card in hole_cards]
        hole_suits = [card[1] if len(card) > 1 else 'S' for card in hole_cards]

        # 1. 高牌加分 (更精确的评分)
        high_cards = {14: 0.08, 13: 0.06, 12: 0.04, 11: 0.03}  # A, K, Q, J
        for rank in hole_ranks:
            if rank in high_cards:
                strength += high_cards[rank]

        # 2. 对子加分 (根据对子大小调整)
        if hole_ranks[0] == hole_ranks[1]:
            if hole_ranks[0] >= 10:  # TT以上的高对
                pair_strength = 0.25 + (hole_ranks[0] - 10) * 0.05
            else:  # 中低对
                pair_strength = 0.1 + (hole_ranks[0] - 2) * 0.02
            strength += min(pair_strength, 0.4)

        # 3. 同花可能性
        if hole_suits[0] == hole_suits[1]:
            strength += 0.03
            # 检查同花听牌
            suit_count = suits.count(hole_suits[0])
            if suit_count >= 4:
                strength += 0.12

        # 4. 顺子可能性 (更精确)
        rank_diff = abs(hole_ranks[0] - hole_ranks[1])
        if rank_diff <= 4 and rank_diff >= 1:
            if rank_diff == 1:  # 连牌
                strength += 0.04
            elif rank_diff <= 3:  # 接近连牌
                strength += 0.02

        # 5. 根据公共牌调整
        if len(public_cards) >= 3:
            made_hand_bonus = self._evaluate_made_hands(all_cards)
            strength += made_hand_bonus

        return min(max(strength, 0.1), 0.95)

    def _card_rank(self, card):
        """将牌面转换为数值"""
        if not card or len(card) == 0:
            return 2
        rank_char = card[0].upper()
        rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                   '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return rank_map.get(rank_char, 2)

    def _evaluate_made_hands(self, all_cards):
        """评估已成型的牌型"""
        if len(all_cards) < 5:
            return 0

        ranks = [self._card_rank(card) for card in all_cards]
        suits = [card[1] if len(card) > 1 else 'S' for card in all_cards]

        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        bonus = 0

        # 检查各种牌型 (更精确的评分)
        if max(rank_counts.values()) >= 4:  # 四条
            bonus += 0.35
        elif max(rank_counts.values()) >= 3:  # 三条
            bonus += 0.2
            if len([c for c in rank_counts.values() if c >= 2]) >= 2:  # 葫芦
                bonus += 0.1
        elif len([c for c in rank_counts.values() if c >= 2]) >= 2:  # 两对
            bonus += 0.12
        elif max(rank_counts.values()) >= 2:  # 一对
            # 根据对子大小调整
            pair_rank = max([rank for rank, count in rank_counts.items() if count >= 2])
            if pair_rank >= 10:  # 高对
                bonus += 0.08
            else:  # 低对
                bonus += 0.05

        # 同花
        if max(suit_counts.values()) >= 5:
            bonus += 0.25

        # 顺子检查（简化版）
        sorted_ranks = sorted(set(ranks))
        if len(sorted_ranks) >= 5:
            for i in range(len(sorted_ranks) - 4):
                if sorted_ranks[i+4] - sorted_ranks[i] == 4:
                    bonus += 0.2
                    break

        return bonus

    def calculate_pot_odds(self, data):
        """计算底池赔率"""
        current_bet = data.get('current_bet', 0)
        pot_size = data.get('pot_size', 0)

        if current_bet == 0:
            return float('inf')  # 无需跟注

        return pot_size / current_bet if current_bet > 0 else float('inf')

    def get_position_factor(self, position, total_players):
        """获取位置因子"""
        if total_players == 2:
            return self.position_weights.get(position, 0.85)
        # 多人游戏位置策略可以扩展
        return 0.85

    def should_bluff(self, hand_strength, position_factor):
        """决定是否诈唬"""
        if hand_strength > 0.7:  # 强牌不需要诈唬
            return False

        bluff_threshold = self.bluff_frequency * position_factor
        return random.random() < bluff_threshold

    def make_decision(self, data):
        """
        核心决策函数
        基于手牌强度、位置、底池赔率等因素做出决策
        """
        legal_actions = data.get('legal_actions', [])
        if not legal_actions:
            return 'fold'

        # 获取游戏信息
        hole_cards = data.get('hand', [])
        public_cards = data.get('public_cards', [])
        position = data.get('position', 0)
        total_players = data.get('total_players', 2)

        # 评估手牌强度
        hand_strength = self.evaluate_hand_strength(hole_cards, public_cards)

        # 位置因子
        position_factor = self.get_position_factor(position, total_players)

        # 调整后的手牌强度
        adjusted_strength = hand_strength * position_factor

        # 底池赔率
        pot_odds = self.calculate_pot_odds(data)

        # 决策逻辑
        if 'raise' in legal_actions:
            # 强牌或诈唬时加注
            if adjusted_strength > 0.75 or self.should_bluff(hand_strength, position_factor):
                return 'raise'

        if 'call' in legal_actions:
            # 根据手牌强度和底池赔率决定跟注
            call_threshold = 0.4 + (0.1 if pot_odds > 3 else 0)
            if adjusted_strength > call_threshold:
                return 'call'

        if 'check' in legal_actions:
            # 中等牌力或弱牌时过牌
            if adjusted_strength > 0.3 or hand_strength < 0.2:
                return 'check'

        # 默认弃牌
        if 'fold' in legal_actions:
            return 'fold'

        # 兜底策略
        return legal_actions[0] if legal_actions else 'fold'


# 创建全局AI智能体实例
poker_agent = PokerAgent()


def get_action(data):
    """
    智能决策函数 - 使用PokerAgent进行决策
    """
    print(f"[DEBUG] 收到游戏数据: {data}")

    try:
        # 使用智能智能体进行决策
        action = poker_agent.make_decision(data)
        print(f"[AI决策] 选择动作: {action}")
        return action
    except Exception as e:
        print(f"[ERROR] AI决策出错: {e}")
        # 降级到简单策略
        legal_actions = data.get('legal_actions', [])
        if 'check' in legal_actions:
            return 'check'
        elif 'call' in legal_actions:
            return 'call'
        elif 'fold' in legal_actions:
            return 'fold'
        else:
            return legal_actions[0] if legal_actions else 'fold'


def sendJson(request, jsonData):
    data = json.dumps(jsonData).encode()
    request.send(struct.pack('i', len(data)))
    request.sendall(data)


def recvJson(request):
    data = request.recv(4)
    length = struct.unpack('i', data)[0]
    data = request.recv(length).decode()
    while len(data) != length:
        data = data + request.recv(length - len(data)).decode()
    data = json.loads(data)
    return data


if __name__ == "__main__":
    # 解析命令行参数
    if len(sys.argv) != 4:
        print("使用方法: python client.py <room_number> <name> <game_number>")
        print("例如: python client.py 2 MyAI 10")
        sys.exit(1)

    room_number = int(sys.argv[1])          # 一局游戏人数
    name = sys.argv[2]                      # 当前程序的 AI 名字
    game_number = int(sys.argv[3])          # 最大对局数量

    print(f"启动德州扑克AI: {name}")
    print(f"游戏人数: {room_number}")
    print(f"最大局数: {game_number}")
    print("-" * 40)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    message = dict(info='connect',
                   name=name,
                   room_number=room_number,
                   game_number=game_number)
    sendJson(client, message)
    while True:
        data = recvJson(client)
        if data['info'] == 'state':
            if data['position'] == data['action_position']:
                position = data['position']
                action = get_action(data)
                sendJson(client, {'action': action, 'info': 'action'})
        elif data['info'] == 'result':
            print('win money: {},\tyour card: {},\topp card: {},\t\tpublic card: {}'.format(
                data['players'][position]['win_money'], data['player_card'][position],
                data['player_card'][1 - position], data['public_card']))
            sendJson(client, {'info': 'ready', 'status': 'start'})
        else:
            print(data)
            break
    client.close()
