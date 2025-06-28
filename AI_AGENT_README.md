# 智能德州扑克AI Agent

**作者**: 刘宇轩  田偲

**分工**：
- 代码算法实现：刘宇轩
- 测试和报告：田偲

## 项目概述

根据2024-2025春季人工智能基础课程大作业要求，本项目对原始的`client.py`进行了重构，实现了一个智能的德州扑克AI智能体。

## 项目文件结构与功能
```
poker-master/
├──  2024-2025春季人工智能基础大作业要求.pdf    # 作业要求文档
├──  AI_AGENT_README.md                        # 项目技术文档
├──  README.md                                 # 原始项目说明
├──  client.py                                 # 智能AI客户端 (核心)
├──  serve.py                                  # 游戏服务器
├──  test_agent.py                             # 功能测试脚本
├──  demo_ai.py                                # 决策演示脚本
├──  simple_battle.py                          # 简化对战测试
├──  interactive_test.py                       # 交互式测试
├──  poker.zip                                 # 项目压缩包
├──  __pycache__/                              # Python缓存文件
│   ├── client.cpython-312.pyc
│   └── my_agent.cpython-312.pyc
├──  docs/                                     # 文档目录
│   ├──  seq.png                               # 序列图
│   ├──  德扑程序使用方法.md                    # 使用说明
│   ├──  德扑通信协议.md                        # 通信协议
│   └──  无限注德州扑克游戏规则.md               # 游戏规则
└──  poker/                                    # 游戏引擎模块
    ├── __init__.py
    ├── __pycache__/
    ├── core/                                 # 游戏核心逻辑
    │   ├──  __init__.py
    │   ├──  action.py                         # 动作定义
    │   ├──  card.py                           # 扑克牌相关
    │   ├──  constants.py                      # 常量定义
    │   ├──  history.py                        # 历史记录
    │   ├──  player.py                         # 玩家类
    │   ├──  result.py                         # 结果处理
    │   ├──  state.py                          # 游戏状态
    │   └──  __pycache__/
    ├── host/                                 # 服务器端逻辑
    │   ├──  __init__.py
    │   ├──  config.py                         # 配置文件
    │   ├──  game.py                           # 游戏逻辑
    │   ├──  host.py                           # 主机服务
    │   ├──  player.py                         # 服务器端玩家
    │   ├──  utils.py                          # 工具函数
    │   └──  __pycache__/
    └──  ia/                                   # AI相关模块
        ├──  __init__.py
        ├──  action.py                         # AI动作
        ├──  builders.py                       # 构建器
        ├──  env.py                            # 环境设置
        ├──  utils.py                          # AI工具函数
        └──  __pycache__/
```

### 核心文件

#### client.py - 智能AI客户端
项目的核心文件，包含重构后的智能德州扑克AI。主要功能包括：
- PokerAgent类 - 智能AI代理
- evaluate_hand_strength() - 手牌强度评估算法
- make_decision() - 核心决策逻辑
- get_action() - 重构后的智能决策函数
- 网络通信功能，用于连接游戏服务器
```
client.py
├── PokerAgent类
│   ├── __init__()           # 初始化参数
│   ├── evaluate_hand_strength()  # 手牌评估
│   ├── calculate_pot_odds()      # 赔率计算
│   ├── get_position_factor()     # 位置因子
│   ├── should_bluff()           # 诈唬判断
│   └── make_decision()          # 核心决策
├── get_action()             # 重构后的决策接口
└── 原有网络通信代码
```
#### serve.py - 游戏服务器
启动德州扑克游戏服务器，监听端口2333，管理多个客户端连接和游戏流程。

### 测试与演示文件

#### test_agent.py - 功能测试脚本
验证AI代理的各项功能，包括手牌强度评估准确性、决策逻辑正确性、底池赔率计算等。

#### demo_ai.py - 决策演示脚本
展示AI在不同场景下的决策过程，模拟4个典型场景，显示AI的分析思路。

#### simple_battle.py - 简化对战测试
直接模拟两个AI对战，不依赖服务器。提供完整的游戏流程模拟、详细的决策过程展示和战绩统计。

#### interactive_test.py - 交互式测试
人机对战测试环境，允许用户与AI进行交互式德州扑克对战。

## 使用方法

### 1. 功能测试

#### 基础功能验证
```bash
python test_agent.py
```
运行完整的功能测试套件，验证AI代理的各项核心功能：
- 手牌强度评估算法测试
- 决策逻辑正确性验证
- 底池赔率计算准确性检查
- 各种场景下的AI表现测试

#### AI决策演示
```bash
python demo_ai.py
```
展示AI在4个典型场景下的决策过程：
- 强牌AA vs 弱公共牌
- 垃圾牌27 vs 高公共牌
- 中等牌89 vs 中等公共牌
- 同花听牌决策分析

### 2. AI对战测试

#### 简化对战测试
```bash
python simple_battle.py
```
直接模拟两个AI对战，无需服务器：
- 完整的游戏流程模拟
- 详细的决策过程展示
- 自动战绩统计
- 支持自定义对战局数

#### 服务器模式对战
**步骤1**: 启动游戏服务器
```bash
python serve.py
```

**步骤2**: 启动第一个AI客户端
```bash
python client.py 2 SmartAI 5
```

**步骤3**: 启动第二个AI客户端
```bash
python client.py 2 TestAI 5
```

**参数说明**:
- `2`: 游戏人数（支持2人对战）
- `SmartAI/TestAI`: AI名称（可自定义）
- `5`: 最大对局数

#### 自动化对战观察
```bash
python watch_battle.py
```
自动启动服务器和两个AI进行对战：
- 自动管理服务器启动和关闭
- 收集完整的对战数据
- 显示详细的对战记录

**注：** 实际操作中经常因为服务器不稳定导致连接失败，需要多试几次。

推荐直接使用`simple_battle.py`进行对战测试，方便快捷。

### 3. 交互式测试

#### 人机对战
```bash
python interactive_test.py
```
与AI进行交互式德州扑克对战：
- 查看自己的手牌和公共牌
- 选择`fold/check/call/raise`动作
- 观察AI的决策过程
- 体验完整的游戏流程

## 核心特性

### 1. 智能决策系统
- **手牌强度评估**: 基于牌型、高牌、对子等多维度评估
- **位置策略**: 根据座位位置调整决策激进程度
- **底池赔率计算**: 考虑投入成本与潜在收益
- **诈唬机制**: 适度的诈唬策略增加不可预测性

### 2. 手牌评估算法
```python
def evaluate_hand_strength(self, hole_cards, public_cards):
    # 基础强度评估
    # 高牌加分 (A, K, Q, J)
    # 对子识别与评分
    # 同花/顺子潜力分析
    # 已成型牌型检测 (四条、三条、两对等)
```

### 3. 决策逻辑
- **强牌 (>0.75强度)**: 倾向于加注
- **中等牌 (0.4-0.75)**: 根据底池赔率决定跟注/过牌
- **弱牌 (<0.4)**: 倾向于弃牌或过牌
- **诈唬策略**: 15%概率在合适位置进行诈唬

### 4. 策略特征
- **紧凶型**: 选择性进入底池，进入后积极争取
- **位置敏感**: 后位更加激进，前位相对保守
- **适应性强**: 根据牌局情况动态调整

### 5. 预期表现
- **对抗随机策略**: 显著优势
- **对抗简单规则策略**: 明显优势
- **对抗复杂AI**: 具备竞争力

## 技术实现

### 核心类: PokerAgent
```python
class PokerAgent:
    def __init__(self):
        self.aggression_factor = 0.3    # 激进程度
        self.bluff_frequency = 0.15     # 诈唬频率
        self.tight_factor = 0.6         # 紧凶程度
        
    def make_decision(self, data):
        # 综合决策逻辑
        pass
```

### 主要方法
1. `evaluate_hand_strength()` - 手牌强度评估
2. `calculate_pot_odds()` - 底池赔率计算
3. `get_position_factor()` - 位置因子获取
4. `should_bluff()` - 诈唬决策
5. `make_decision()` - 核心决策函数

### 设计原则
1. **实用性导向**
   - 基于德州扑克理论基础
   - 考虑实际对战场景
   - 平衡风险与收益

2. **代码易读性**
   - 清晰的代码结构
   - 详细的注释说明
   - 模块化设计

## 算法优势

### 1. 多维度评估
- 不仅考虑手牌本身，还考虑位置、底池大小等因素
- 动态调整策略，避免过于机械化

### 2. 风险控制
- 合理的诈唬频率，避免过度激进
- 基于底池赔率的理性决策

### 3. 可扩展性
- 预留对手建模接口
- 支持多人游戏扩展
- 参数可调节，便于优化



### 4. 开发与调试

#### 修改AI参数
在client.py中的PokerAgent类可以调整以下参数：
```python
self.aggression_factor = 0.3  # 激进程度 (0.1-0.5)
self.bluff_frequency = 0.15   # 诈唬频率 (0.05-0.25)
self.tight_factor = 0.6       # 紧凶程度 (0.4-0.8)
```

#### 添加自定义策略
可以在make_decision()方法中添加自定义的决策逻辑：
- 对手建模
- 历史行为分析
- 高级数学模型

### 5. 性能评估

#### 批量测试
运行多次simple_battle.py来评估AI性能：
```bash
# 运行10局对战
python simple_battle.py
# 输入: 10

# 分析胜率和决策质量
```

#### 参数优化
通过调整AI参数并测试性能来优化策略：
1. 修改`aggression_factor`
2. 运行`simple_battle.py`测试
3. 记录胜率变化
4. 重复优化过程

## 后续优化方向

1. **对手建模**: 分析对手行为模式
2. **深度学习**: 引入神经网络优化决策
3. **蒙特卡洛模拟**: 更精确的胜率计算
4. **动态参数调整**: 根据战绩自动优化参数

