#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的AI对战测试
直接模拟两个AI对战，不依赖服务器
"""

import sys
import os
import random
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import PokerAgent

class SimpleBattle:
    def __init__(self):
        self.ai1 = PokerAgent()
        self.ai2 = PokerAgent()
        self.deck = self.create_deck()
        
    def create_deck(self):
        """创建一副牌"""
        suits = ['S', 'H', 'D', 'C']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        deck = [rank + suit for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck
    
    def deal_hands(self):
        """发手牌"""
        ai1_hand = [self.deck.pop(), self.deck.pop()]
        ai2_hand = [self.deck.pop(), self.deck.pop()]
        return ai1_hand, ai2_hand
    
    def deal_community(self):
        """发公共牌"""
        flop = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        turn = self.deck.pop()
        river = self.deck.pop()
        return flop, turn, river
    
    def simulate_game(self, game_num):
        """模拟一局游戏"""
        print(f"\n=== 第{game_num}局 ===")
        
        # 重新洗牌
        self.deck = self.create_deck()
        
        # 发牌
        ai1_hand, ai2_hand = self.deal_hands()
        flop, turn, river = self.deal_community()
        
        print(f"AI1手牌: {' '.join(ai1_hand)}")
        print(f"AI2手牌: {' '.join(ai2_hand)}")
        
        # 模拟各个阶段的决策
        stages = [
            ("翻牌前", []),
            ("翻牌", flop),
            ("转牌", flop + [turn]),
            ("河牌", flop + [turn, river])
        ]
        
        pot = 0
        ai1_bet = 0
        ai2_bet = 0
        
        for stage_name, public_cards in stages:
            print(f"\n--- {stage_name} ---")
            if public_cards:
                print(f"公共牌: {' '.join(public_cards)}")
            
            # AI1决策
            ai1_data = {
                'hand': ai1_hand,
                'public_cards': public_cards,
                'legal_actions': ['fold', 'check', 'call', 'raise'],
                'position': 0,
                'total_players': 2,
                'current_bet': 0,
                'pot_size': pot
            }
            
            ai1_action = self.ai1.make_decision(ai1_data)
            print(f"AI1决策: {ai1_action}")
            
            # AI2决策
            ai2_data = {
                'hand': ai2_hand,
                'public_cards': public_cards,
                'legal_actions': ['fold', 'check', 'call', 'raise'],
                'position': 1,
                'total_players': 2,
                'current_bet': 0,
                'pot_size': pot
            }
            
            ai2_action = self.ai2.make_decision(ai2_data)
            print(f"AI2决策: {ai2_action}")
            
            # 简化的下注逻辑
            if ai1_action == 'fold':
                print("AI1弃牌，AI2获胜")
                return 'ai2_win'
            elif ai2_action == 'fold':
                print("AI2弃牌，AI1获胜")
                return 'ai1_win'
            elif ai1_action == 'raise':
                pot += 20
                ai1_bet += 20
            elif ai2_action == 'raise':
                pot += 20
                ai2_bet += 20
        
        # 摊牌比较
        print(f"\n--- 摊牌 ---")
        final_public = flop + [turn, river]
        print(f"最终公共牌: {' '.join(final_public)}")
        
        ai1_strength = self.ai1.evaluate_hand_strength(ai1_hand, final_public)
        ai2_strength = self.ai2.evaluate_hand_strength(ai2_hand, final_public)
        
        print(f"AI1牌力: {ai1_strength:.3f}")
        print(f"AI2牌力: {ai2_strength:.3f}")
        
        if ai1_strength > ai2_strength:
            print("AI1获胜！")
            return 'ai1_win'
        elif ai2_strength > ai1_strength:
            print("AI2获胜！")
            return 'ai2_win'
        else:
            print("平局！")
            return 'tie'
    
    def run_battle(self, num_games=5):
        """运行对战"""
        print("简化AI对战测试")
        print("=" * 50)
        
        ai1_wins = 0
        ai2_wins = 0
        ties = 0
        
        for i in range(1, num_games + 1):
            result = self.simulate_game(i)
            
            if result == 'ai1_win':
                ai1_wins += 1
            elif result == 'ai2_win':
                ai2_wins += 1
            else:
                ties += 1
            
            print(f"当前战绩 - AI1: {ai1_wins}胜, AI2: {ai2_wins}胜, 平局: {ties}")
            
            if i < num_games:
                input("\n按回车继续下一局...")
        
        print(f"\n=== 最终战绩 ===")
        print(f"AI1: {ai1_wins}胜 ({ai1_wins/num_games*100:.1f}%)")
        print(f"AI2: {ai2_wins}胜 ({ai2_wins/num_games*100:.1f}%)")
        print(f"平局: {ties}局 ({ties/num_games*100:.1f}%)")
        
        if ai1_wins > ai2_wins:
            print("AI1总体获胜！")
        elif ai2_wins > ai1_wins:
            print("AI2总体获胜！")
        else:
            print("总体平局！")

if __name__ == "__main__":
    battle = SimpleBattle()
    
    try:
        games_input = input("输入对战局数 (默认5局): ").strip()
        games = int(games_input) if games_input.isdigit() else 5
        
        battle.run_battle(games)
        
    except KeyboardInterrupt:
        print("\n用户中断对战")
    
    print("\n按回车键退出...")
    input()
