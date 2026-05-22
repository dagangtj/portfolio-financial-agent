"""
测试：资金监控模块
"""
import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from examples.balance_monitor import SimpleBalanceMonitor

class TestBalanceMonitor:
    """测试资金监控功能"""
    
    def test_initialization(self):
        monitor = SimpleBalanceMonitor(platforms=['binance'])
        assert monitor.platforms == ['binance']
        assert monitor.check_interval == 300
        assert monitor.running == False
    
    def test_thresholds(self):
        monitor = SimpleBalanceMonitor()
        assert 'total_usd_min' in monitor.thresholds
        assert monitor.thresholds['total_usd_min'] == 1000
    
    @pytest.mark.asyncio
    async def test_fetch_balances(self):
        monitor = SimpleBalanceMonitor()
        balances = await monitor.fetch_balances()
        
        assert isinstance(balances, dict)
        assert 'binance' in balances
        assert 'total_usd' in balances['binance']
        assert balances['binance']['total_usd'] > 0
    
    def test_check_alerts_low_balance(self):
        monitor = SimpleBalanceMonitor()
        monitor.thresholds['total_usd_min'] = 50000
        
        balances = {
            'binance': {'BTC': 0.1, 'total_usd': 10000}
        }
        
        alerts = monitor.check_alerts(balances)
        assert len(alerts) > 0
        assert '低于阈值' in alerts[0]
    
    def test_check_alerts_normal(self):
        monitor = SimpleBalanceMonitor()
        
        balances = {
            'binance': {'BTC': 0.5, 'total_usd': 50000}
        }
        
        alerts = monitor.check_alerts(balances)
        assert len(alerts) == 0  # 正常情况不应告警

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
