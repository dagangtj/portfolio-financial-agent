"""
测试：投资组合模块
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from examples.portfolio_report import PortfolioReport

class TestPortfolioReport:
    """测试投资组合报告功能"""
    
    def test_initialization(self):
        assets = ['BTC', 'ETH']
        report = PortfolioReport(assets)
        assert report.assets == assets
    
    def test_fetch_prices(self):
        report = PortfolioReport(['BTC'])
        prices = report.fetch_prices()
        
        assert isinstance(prices, dict)
        assert 'BTC' in prices
        assert prices['BTC'] > 0
    
    def test_calculate_metrics(self):
        report = PortfolioReport(['BTC', 'ETH'])
        holdings = {'BTC': 1.0, 'ETH': 10.0}
        
        metrics = report.calculate_metrics(holdings)
        
        assert 'total_value' in metrics
        assert 'allocations' in metrics
        assert metrics['total_value'] > 0
        assert 'BTC' in metrics['allocations']
        assert 'weight' in metrics['allocations']['BTC']
    
    def test_generate_report(self):
        report = PortfolioReport(['BTC'])
        holdings = {'BTC': 1.0}
        
        md = report.generate_markdown_report(holdings)
        
        assert isinstance(md, str)
        assert '# 📊 投资组合报告' in md
        assert 'BTC' in md
        assert '$' in md
    
    def test_report_saves_file(self, tmp_path):
        report = PortfolioReport(['BTC'])
        holdings = {'BTC': 1.0}
        
        md = report.generate_markdown_report(holdings)
        test_file = tmp_path / "test_report.md"
        
        report.save_report(md, str(test_file))
        assert test_file.exists()

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
