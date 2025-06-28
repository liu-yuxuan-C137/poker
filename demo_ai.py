#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克AI决策演示
展示不同情况下AI的决策过程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 模拟client.py中的PokerAgent类
import random
import math
from collections import Counter

class PokerAgent:
    """智能德州扑克AI代理"""
    
    def __init__(self):
        self.aggression_factor = 0.3
        self.bluff_frequency = 0.15
        self.tight_factor = 0.6
        self.opponent_stats = {}
        self.game_history = []
        self.position_weights = {0: 0.8, 1: 0.9}
    
    def evaluate_hand_strength(self, hole_cards, public_cards):
        if not hole_cards or len(hole_cards) != 2:
            return 0.5
            
        all_cards = hole_cards + public_cards
        strength = 0.5
        
        ranks = [self._card_rank(card) for card in all_cards]
        suits = [card[1] if len(card) > 1 else 'S' for card in all_cards]
        
        hole_ranks = [self._card_rank(card) for card in hole_cards]
        hole_suits = [card[1] if len(card) > 1 else 'S' for card in hole_cards]
        
        # 高牌加分
        high_cards = [14, 13, 12, 11]
        for rank in hole_ranks:
            if rank in high_cards:
                strength += 0.1
        
        # 对子加分
        if hole_ranks[0] == hole_ranks[1]:
            pair_strength = min(hole_ranks[0] / 14.0, 0.3)
            strength += pair_strength
        
        # 同花可能性
        if hole_suits[0] == hole_suits[1]:
            strength += 0.05
            suit_count = suits.count(hole_suits[0])
            if suit_count >= 4:
                strength += 0.15
        
        # 顺子可能性
        if abs(hole_ranks[0] - hole_ranks[1]) <= 4:
            strength += 0.05
        
        # 根据公共牌调整
        if len(public_cards) >= 3:
            strength += self._evaluate_made_hands(all_cards)
        
        return min(max(strength, 0.1), 0.95)
    
    def _card_rank(self, card):
        if not card or len(card) == 0:
            return 2
        rank_char = card[0].upper()
        rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                   '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return rank_map.get(rank_char, 2)
    
    def _evaluate_made_hands(self, all_cards):
        if len(all_cards) < 5:
            return 0
            
        ranks = [self._card_rank(card) for card in all_cards]
        suits = [card[1] if len(card) > 1 else 'S' for card in all_cards]
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        bonus = 0
        
        if max(rank_counts.values()) >= 4:
            bonus += 0.4
        elif max(rank_counts.values()) >= 3:
            bonus += 0.25
            if len([c for c in rank_counts.values() if c >= 2]) >= 2:
                bonus += 0.15
        elif len([c for c in rank_counts.values() if c >= 2]) >= 2:
            bonus += 0.15
        elif max(rank_counts.values()) >= 2:
            bonus += 0.1
        
        if max(suit_counts.values()) >= 5:
            bonus += 0.3
        
        sorted_ranks = sorted(set(ranks))
        if len(sorted_ranks) >= 5:
            for i in range(len(sorted_ranks) - 4):
                if sorted_ranks[i+4] - sorted_ranks[i] == 4:
                    bonus += 0.25
                    break
        
        return bonus
    
    def calculate_pot_odds(self, data):
        current_bet = data.get('current_bet', 0)
        pot_size = data.get('pot_size', 0)
        
        if current_bet == 0:
            return float('inf')
        
        return pot_size / current_bet if current_bet > 0 else float('inf')
    
    def get_position_factor(self, position, total_players):
        if total_players == 2:
            return self.position_weights.get(position, 0.85)
        return 0.85
    
    def should_bluff(self, hand_strength, position_factor):
        if hand_strength > 0.7:
            return False
        
        bluff_threshold = self.bluff_frequency * position_factor
        return random.random() < bluff_threshold
    
    def make_decision(self, data):
        legal_actions = data.get('legal_actions', [])
        if not legal_actions:
            return 'fold'
        
        hole_cards = data.get('hand', [])
        public_cards = data.get('public_cards', [])
        position = data.get('position', 0)
        total_players = data.get('total_players', 2)
        
        hand_strength = self.evaluate_hand_strength(hole_cards, public_cards)
        position_factor = self.get_position_factor(position, total_players)
        adjusted_strength = hand_strength * position_factor
        pot_odds = self.calculate_pot_odds(data)
        
        print(f"  手牌强度: {hand_strength:.3f}")
        print(f"  位置因子: {position_factor:.3f}")
        print(f"  调整强度: {adjusted_strength:.3f}")
        print(f"  底池赔率: {pot_odds:.1f}" if pot_odds != float('inf') else "  底池赔率: 无需跟注")
        
        if 'raise' in legal_actions:
            if adjusted_strength > 0.75 or self.should_bluff(hand_strength, position_factor):
                return 'raise'
        
        if 'call' in legal_actions:
            call_threshold = 0.4 + (0.1 if pot_odds > 3 else 0)
            if adjusted_strength > call_threshold:
                return 'call'
        
        if 'check' in legal_actions:
            if adjusted_strength > 0.3 or hand_strength < 0.2:
                return 'check'
        
        if 'fold' in legal_actions:
            return 'fold'
        
        return legal_actions[0] if legal_actions else 'fold'

def demo_scenarios():
    """演示不同场景下的AI决策"""
    print("德州扑克AI决策演示")
    print("=" * 60)
    
    agent = PokerAgent()
    
    scenarios = [
        {
            'name': '场景1: 强牌AA vs 弱公共牌',
            'data': {
                'hand': ['AS', 'AH'],
                'public_cards': ['2C', '7D', '9S'],
                'legal_actions': ['fold', 'call', 'raise'],
                'position': 1,
                'total_players': 2,
                'current_bet': 10,
                'pot_size': 30
            }
        },
        {
            'name': '场景2: 垃圾牌27 vs 高公共牌',
            'data': {
                'hand': ['2S', '7H'],
                'public_cards': ['KC', 'QD', 'JS'],
                'legal_actions': ['fold', 'call'],
                'position': 0,
                'total_players': 2,
                'current_bet': 20,
                'pot_size': 40
            }
        },
        {
            'name': '场景3: 中等牌89 vs 中等公共牌',
            'data': {
                'hand': ['8S', '9H'],
                'public_cards': ['2C', '7D', 'KS'],
                'legal_actions': ['check', 'fold', 'raise'],
                'position': 1,
                'total_players': 2,
                'current_bet': 0,
                'pot_size': 20
            }
        },
        {
            'name': '场景4: 同花听牌',
            'data': {
                'hand': ['AS', 'KS'],
                'public_cards': ['2S', '7S', '9H'],
                'legal_actions': ['fold', 'call', 'raise'],
                'position': 1,
                'total_players': 2,
                'current_bet': 15,
                'pot_size': 45
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{scenario['name']}")
        print("-" * 40)

        data = scenario['data']
        print(f"手牌: {' '.join(data['hand'])}")
        print(f"公共牌: {' '.join(data['public_cards'])}")
        print(f"可选动作: {', '.join(data['legal_actions'])}")
        print(f"位置: {data['position']}, 当前下注: {data['current_bet']}, 底池: {data['pot_size']}")

        print("\nAI分析:")
        decision = agent.make_decision(data)
        print(f"  最终决策: {decision.upper()}")
        
        if i < len(scenarios):
            print()

if __name__ == "__main__":
    demo_scenarios()
