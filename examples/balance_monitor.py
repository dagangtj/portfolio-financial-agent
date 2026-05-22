"""
示例：资金监控器
展示如何使用 Financial Agent 监控多平台资产
"""
import os
import asyncio
from datetime import datetime

class SimpleBalanceMonitor:
    """简化版资金监控示例"""
    
    def __init__(self, platforms=None, check_interval=300):
        self.platforms = platforms or ['binance']
        self.check_interval = check_interval  # 秒
        self.balances = {}
        self.thresholds = {
            'total_usd_min': 1000,
            'alert_drop_pct': 10
        }
        self.running = False
    
    async def fetch_balances(self):
        """模拟从交易所获取余额"""
        # 实际使用中会调用 CCXT 库
        # import ccxt
        # exchange = ccxt.binance({'apiKey': ..., 'secret': ...})
        # return exchange.fetch_balance()
        
        return {
            'binance': {
                'BTC': 0.5,
                'ETH': 5.0,
                'USDT': 10000,
                'total_usd': 45000
            },
            'okx': {
                'BTC': 0.3,
                'ETH': 3.0,
                'USDT': 5000,
                'total_usd': 28000
            }
        }
    
    def check_alerts(self, balances):
        """检查是否需要告警"""
        total = sum(b.get('total_usd', 0) for b in balances.values())
        
        alerts = []
        if total < self.thresholds['total_usd_min']:
            alerts.append(f"⚠️ 总资产低于阈值: ${total:,.2f} < ${self.thresholds['total_usd_min']}")
        
        # 检查单个资产占比
        for platform, data in balances.items():
            btc_value = data.get('BTC', 0) * 65000  # 假设价格
            if btc_value > total * 0.5:
                alerts.append(f"⚠️ {platform} BTC占比过高: {btc_value/total*100:.1f}%")
        
        return alerts
    
    async def run(self):
        """主循环"""
        self.running = True
        print(f"[{datetime.now()}] 资金监控已启动")
        
        while self.running:
            try:
                balances = await self.fetch_balances()
                self.balances = balances
                
                total = sum(b.get('total_usd', 0) for b in balances.values())
                print(f"[{datetime.now()}] 总资产: ${total:,.2f}")
                
                alerts = self.check_alerts(balances)
                for alert in alerts:
                    print(f"  🔔 {alert}")
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ 错误: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        self.running = False


if __name__ == '__main__':
    monitor = SimpleBalanceMonitor(
        platforms=['binance', 'okx'],
        check_interval=10  # 10秒演示用
    )
    
    try:
        asyncio.run(monitor.run())
    except KeyboardInterrupt:
        monitor.stop()
        print("\n监控已停止")
