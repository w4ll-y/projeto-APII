from abc import ABC, abstractmethod

class InputInterface(ABC):
    @abstractmethod
    def is_walk_up(self) -> bool:
        pass

    @abstractmethod
    def is_walk_down(self) -> bool:
        pass
    
    @abstractmethod
    def is_walk_left(self) -> bool:
        pass
    
    @abstractmethod
    def is_walk_right(self) -> bool:
        pass

    @abstractmethod
    def is_frst_attacking(self) -> bool:
        pass
    
    @abstractmethod
    def is_scd_attacking(self) -> bool:
        pass

    @abstractmethod
    def is_changing_weapon(self) -> bool:
        pass

    @abstractmethod
    def is_interacting(self) -> bool:
        pass

    @abstractmethod
    def is_pausing(self) -> bool:
        pass

    @abstractmethod
    def is_unpausing(self) -> bool:
        pass

    @abstractmethod
    def is_selecting(self) -> bool:
        pass