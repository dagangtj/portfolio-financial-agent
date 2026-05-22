"""
示例：投资组合报告生成
展示如何生成专业的投资组合分析报告
"""
from datetime import datetime
import json

class PortfolioReport:
    """投资组合报告生成器"""
    
    def __init__(self, assets):
        self.assets = assets
        self.prices = {}
    
    def fetch_prices(self):
        """模拟获取实时价格"""
        return {
            'BTC': 65000.00,
            'ETH': 3500.00,
            'SOL': 145.00,
            'AAPL': 190.00,
            'TSLA': 175.00
        }
    
    def calculate_metrics(self, holdings):
        """计算投资组合指标"""
        prices = self.fetch_prices()
        
        total_value = 0
        allocations = {}
        
        for asset, quantity in holdings.items():
            price = prices.get(asset, 0)
            value = quantity * price
            total_value += value
            allocations[asset] = {
                'quantity': quantity,
                'price': price,
                'value': value
            }
        
        # 计算占比
        for asset in allocations:
            allocations[asset]['weight'] = allocations[asset]['value'] / total_value if total_value > 0 else 0
        
        return {
            'total_value': total_value,
            'allocations': allocations,
            'asset_count': len(holdings)
        }
    
    def generate_markdown_report(self, holdings):
        """生成 Markdown 格式的报告"""
        metrics = self.calculate_metrics(holdings)
        
        report = f"""# 📊 投资组合报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 💰 资产概览

| 资产 | 数量 | 单价 | 价值 | 占比 |
|------|------|------|------|------|
"""
        
        for asset, data in metrics['allocations'].items():
            report += f"| {asset} | {data['quantity']:.4f} | ${data['price']:,.2f} | ${data['value']:,.2f} | {data['weight']*100:.1f}% |\n"
        
        report += f"""
**总资产价值**: ${metrics['total_value']:,.2f}
**持有资产数**: {metrics['asset_count']}

## 📈 风险评估

- **集中度风险**: {'高' if any(a['weight'] > 0.5 for a in metrics['allocations'].values()) else '中' if any(a['weight'] > 0.3 for a in metrics['allocations'].values()) else '低'}
- **建议**: 定期再平衡，避免单一资产占比过高

---
*由 Financial Monitoring Agent 自动生成*
"""
        return report
    
    def save_report(self, report, filename=None):
        """保存报告到文件"""
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 报告已保存: {filename}")


if __name__ == '__main__':
    # 示例持仓
    holdings = {
        'BTC': 0.8,
        'ETH': 8.0,
        'SOL': 100.0,
        'AAPL': 50.0,
        'TSLA': 30.0
    }
    
    report_gen = PortfolioReport(list(holdings.keys()))
    report = report_gen.generate_markdown_report(holdings)
    
    print(report)
    report_gen.save_report(report)
