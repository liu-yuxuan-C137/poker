#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德州扑克AI代理测试脚本
用于验证PokerAgent的决策逻辑
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from client import PokerAgent

def test_hand_strength_evaluation():
    """测试手牌强度评估"""
    print("=== 测试手牌强度评估 ===")
    
    agent = PokerAgent()
    
    # 测试用例
    test_cases = [
        {
            'name': '高对AA',
            'hole_cards': ['AS', 'AH'],
            'public_cards': ['2C', '7D', '9S'],
            'expected_range': (0.7, 1.0)
        },
        {
            'name': '中对88',
            'hole_cards': ['8S', '8H'],
            'public_cards': ['2C', '7D', '9S'],
            'expected_range': (0.6, 0.8)
        },
        {
            'name': '高牌AK',
            'hole_cards': ['AS', 'KH'],
            'public_cards': ['2C', '7D', '9S'],
            'expected_range': (0.5, 0.7)
        },
        {
            'name': '垃圾牌27',
            'hole_cards': ['2S', '7H'],
            'public_cards': ['KC', 'QD', 'JS'],
            'expected_range': (0.1, 0.5)
        }
    ]
    
    for case in test_cases:
        strength = agent.evaluate_hand_strength(case['hole_cards'], case['public_cards'])
        min_expected, max_expected = case['expected_range']
        
        print(f"{case['name']}: 强度={strength:.3f}, 期望范围=[{min_expected}, {max_expected}]", end="")
        
        if min_expected <= strength <= max_expected:
            print(" ✓")
        else:
            print(" ✗")

def test_decision_making():
    """测试决策制定"""
    print("\n=== 测试决策制定 ===")
    
    agent = PokerAgent()
    
    # 测试用例
    test_cases = [
        {
            'name': '强牌应该加注',
            'data': {
                'hand': ['AS', 'AH'],
                'public_cards': ['2C', '7D', '9S'],
                'legal_actions': ['fold', 'call', 'raise'],
                'position': 1,
                'total_players': 2,
                'current_bet': 10,
                'pot_size': 30
            },
            'expected_actions': ['raise', 'call']
        },
        {
            'name': '垃圾牌应该弃牌',
            'data': {
                'hand': ['2S', '7H'],
                'public_cards': ['KC', 'QD', 'JS'],
                'legal_actions': ['fold', 'call'],
                'position': 0,
                'total_players': 2,
                'current_bet': 20,
                'pot_size': 40
            },
            'expected_actions': ['fold']
        },
        {
            'name': '中等牌可以过牌',
            'data': {
                'hand': ['8S', '9H'],
                'public_cards': ['2C', '7D', 'KS'],
                'legal_actions': ['check', 'fold'],
                'position': 1,
                'total_players': 2,
                'current_bet': 0,
                'pot_size': 20
            },
            'expected_actions': ['check']
        }
    ]
    
    for case in test_cases:
        action = agent.make_decision(case['data'])
        print(f"{case['name']}: 决策={action}", end="")
        
        if action in case['expected_actions']:
            print(" ✓")
        else:
            print(f" ✗ (期望: {case['expected_actions']})")

def test_pot_odds_calculation():
    """测试底池赔率计算"""
    print("\n=== 测试底池赔率计算 ===")
    
    agent = PokerAgent()
    
    test_cases = [
        {'current_bet': 10, 'pot_size': 30, 'expected': 3.0},
        {'current_bet': 20, 'pot_size': 40, 'expected': 2.0},
        {'current_bet': 0, 'pot_size': 20, 'expected': float('inf')},
    ]
    
    for case in test_cases:
        data = {'current_bet': case['current_bet'], 'pot_size': case['pot_size']}
        odds = agent.calculate_pot_odds(data)
        
        print(f"跟注{case['current_bet']}, 底池{case['pot_size']}: 赔率={odds}", end="")
        
        if odds == case['expected']:
            print(" ✓")
        else:
            print(f" ✗ (期望: {case['expected']})")

if __name__ == "__main__":
    print("德州扑克AI代理测试")
    print("=" * 50)

    test_hand_strength_evaluation()
    test_decision_making()
    test_pot_odds_calculation()

    print("\n测试完成！")
