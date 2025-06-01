"""
Factory for creating rig mappings.
"""
from .base_mappings import BaseRigMapping
from .mixamo_mapping import MixamoMapping
from .rigify_mapping import RigifyMapping

class RigMappingFactory:
    """Factory for creating rig mappings."""
    
    @staticmethod
    def create_mapping(rig_type: str) -> BaseRigMapping:
        """
        Create a mapping for the specified rig type.
        
        Args:
            rig_type: The type of rig ('MIXAMO', 'RIGIFY', etc.)
            
        Returns:
            A mapping instance for the specified rig type
            
        Raises:
            ValueError: If the rig type is not supported
        """
        mapping_classes = {
            'MIXAMO': MixamoMapping,
            'RIGIFY': RigifyMapping,
            # Add more rig types here
        }
        
        if rig_type not in mapping_classes:
            raise ValueError(f"Unsupported rig type: {rig_type}")
            
        return mapping_classes[rig_type]()
    
    @staticmethod
    def get_supported_rig_types() -> list:
        """Get a list of supported rig types."""
        return ['MIXAMO', 'RIGIFY']  # Add more as they are implemented 