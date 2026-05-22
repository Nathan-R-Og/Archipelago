from typing import Callable, TYPE_CHECKING

from .Options import ArgemiaPlushes
from .Types import VOTVGoal

if TYPE_CHECKING:
    from . import VOTVWorld

def resolve[T](value: T | Callable[[VOTVWorld], T], world: VOTVWorld) -> T:
    return value(world) if callable(value) else value  # type: ignore

def is_goal_enabled(world: VOTVWorld, goal: VOTVGoal):
    return (world.options.objective == goal
        or goal == VOTVGoal.KERFUR_OMEGA and world.options.kerfur_omega_enabled.value
        or goal == VOTVGoal.HELL_ROCK and world.options.hell_rock_enabled.value
        or goal == VOTVGoal.WHITE_ARGEMIA_PLUSH and world.options.argemia_plushes.value >= ArgemiaPlushes.option_rgbycm
        or goal == VOTVGoal.LAMBERT_PLUSH and world.options.lambert_plush_enabled.value
        or goal == VOTVGoal.GREEN_CABINET and world.options.green_cabinet_enabled.value)

def furfur_plush_enabled(world: VOTVWorld):
    return world.options.buried_items.value and world.options.time_sensitive.value
