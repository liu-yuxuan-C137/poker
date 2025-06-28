#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式德州扑克测试
你可以和AI进行对战测试
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import PokerAgent

class InteractivePokerTest:
    def __init__(self):
        self.ai_agent = PokerAgent()
        self.deck = self.create_deck()
        self.pot = 0
        self.player_chips = 1000
        self.ai_chips = 1000
        self.current_bet = 0
        
    def create_deck(self):
        """创建一副牌"""
        suits = ['S', 'H', 'D', 'C']  # 黑桃、红心、方块、梅花
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        deck = [rank + suit for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck
    
    def deal_cards(self):
        """发牌"""
        player_hand = [self.deck.pop(), self.deck.pop()]
        ai_hand = [self.deck.pop(), self.deck.pop()]
        return player_hand, ai_hand
    
    def deal_flop(self):
        """发翻牌"""
        return [self.deck.pop(), self.deck.pop(), self.deck.pop()]
    
    def deal_turn_or_river(self):
        """发转牌或河牌"""
        return self.deck.pop()
    
    def get_player_action(self, legal_actions):
        """获取玩家动作"""
        print(f"\n可选动作: {', '.join(legal_actions)}")
        while True:
            action = input("请选择你的动作 (fold/check/call/raise): ").strip().lower()
            if action in legal_actions:
                return action
            print("无效动作，请重新选择")
    
    def simulate_betting_round(self, player_hand, ai_hand, public_cards, round_name):
        """模拟一轮下注"""
        print(f"\n=== {round_name} ===")
        print(f"你的手牌: {' '.join(player_hand)}")
        if public_cards:
            print(f"公共牌: {' '.join(public_cards)}")
        print(f"底池: {self.pot}, 你的筹码: {self.player_chips}, AI筹码: {self.ai_chips}")
        
        # 玩家行动
        legal_actions = ['fold', 'check', 'call', 'raise'] if self.current_bet == 0 else ['fold', 'call', 'raise']
        if self.current_bet == 0:
            legal_actions.remove('call')
        
        player_action = self.get_player_action(legal_actions)
        
        if player_action == 'fold':
            print("你弃牌了")
            return 'fold'
        elif player_action == 'raise':
            raise_amount = int(input("加注金额: "))
            self.current_bet += raise_amount
            self.player_chips -= raise_amount
            self.pot += raise_amount
            print(f"你加注 {raise_amount}")
        elif player_action == 'call' and self.current_bet > 0:
            self.player_chips -= self.current_bet
            self.pot += self.current_bet
            print(f"你跟注 {self.current_bet}")
        
        # AI行动
        ai_data = {
            'hand': ai_hand,
            'public_cards': public_cards,
            'legal_actions': ['fold', 'check', 'call', 'raise'],
            'position': 1,
            'total_players': 2,
            'current_bet': self.current_bet,
            'pot_size': self.pot
        }
        
        ai_action = self.ai_agent.make_decision(ai_data)
        print(f"AI选择: {ai_action}")
        
        if ai_action == 'fold':
            print("AI弃牌")
            return 'ai_fold'
        elif ai_action == 'raise':
            raise_amount = 20  # AI固定加注20
            self.current_bet += raise_amount
            self.ai_chips -= raise_amount
            self.pot += raise_amount
            print(f"AI加注 {raise_amount}")
        elif ai_action == 'call' and self.current_bet > 0:
            self.ai_chips -= self.current_bet
            self.pot += self.current_bet
            print(f"AI跟注 {self.current_bet}")
        
        return 'continue'
    
    def play_hand(self):
        """进行一手牌"""
        print("\n" + "="*50)
        print("开始新的一手牌")
        print("="*50)
        
        # 重置
        self.deck = self.create_deck()
        self.pot = 0
        self.current_bet = 0
        
        # 发手牌
        player_hand, ai_hand = self.deal_cards()
        
        # 翻牌前
        result = self.simulate_betting_round(player_hand, ai_hand, [], "翻牌前")
        if result in ['fold', 'ai_fold']:
            return result
        
        # 翻牌
        flop = self.deal_flop()
        result = self.simulate_betting_round(player_hand, ai_hand, flop, "翻牌")
        if result in ['fold', 'ai_fold']:
            return result
        
        # 转牌
        turn = self.deal_turn_or_river()
        public_cards = flop + [turn]
        result = self.simulate_betting_round(player_hand, ai_hand, public_cards, "转牌")
        if result in ['fold', 'ai_fold']:
            return result
        
        # 河牌
        river = self.deal_turn_or_river()
        public_cards = flop + [turn, river]
        result = self.simulate_betting_round(player_hand, ai_hand, public_cards, "河牌")
        if result in ['fold', 'ai_fold']:
            return result
        
        # 摊牌
        print(f"\n=== 摊牌 ===")
        print(f"你的手牌: {' '.join(player_hand)}")
        print(f"AI手牌: {' '.join(ai_hand)}")
        print(f"公共牌: {' '.join(public_cards)}")
        
        # 简化的胜负判断（这里可以扩展为完整的牌型比较）
        player_strength = self.ai_agent.evaluate_hand_strength(player_hand, public_cards)
        ai_strength = self.ai_agent.evaluate_hand_strength(ai_hand, public_cards)
        
        print(f"你的牌力: {player_strength:.3f}")
        print(f"AI牌力: {ai_strength:.3f}")
        
        if player_strength > ai_strength:
            print("你赢了这手牌！")
            self.player_chips += self.pot
            return 'player_win'
        else:
            print("AI赢了这手牌！")
            self.ai_chips += self.pot
            return 'ai_win'
    
    def run(self):
        """运行交互式测试"""
        print("欢迎来到德州扑克AI对战测试！")
        print("你将与智能AI进行对战")
        print("输入 'quit' 随时退出游戏")
        
        while True:
            if input("\n按回车开始新的一手牌，或输入 'quit' 退出: ").strip().lower() == 'quit':
                break
                
            result = self.play_hand()
            print(f"\n当前筹码 - 你: {self.player_chips}, AI: {self.ai_chips}")
            
            if self.player_chips <= 0:
                print("你的筹码用完了！游戏结束")
                break
            elif self.ai_chips <= 0:
                print("AI的筹码用完了！你获得了最终胜利！")
                break

if __name__ == "__main__":
    game = InteractivePokerTest()
    game.run()
