from .isolation import IsolationBackDesign
from .perspective import PerspectiveBackDesign
from .hybrid import HybridBackDesign


def create_back_design(grid_type: str):
    """裏面デザインのタイプに応じたインスタンスを生成"""
    design_map = {
        "isolation": IsolationBackDesign,
        "perspective": PerspectiveBackDesign,
        "hybrid": HybridBackDesign
    }
    
    design_class = design_map.get(grid_type)
    if not design_class:
        raise ValueError(f"Unknown grid type: {grid_type}")
    
    return design_class()
