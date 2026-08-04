from dataclasses import dataclass
from typing import Any, Callable, TYPE_CHECKING, TypeVar, override

from rule_builder.field_resolvers import FieldResolver

from .Types import VOTVGoal
from .Constants import max_days

if TYPE_CHECKING:
    from . import VOTVWorld

T = TypeVar('T')
def resolve(value: T | Callable[["VOTVWorld"], T], world: "VOTVWorld") -> T:
    return value(world) if callable(value) else value  # type: ignore

def is_goal_enabled(world: "VOTVWorld", goal: VOTVGoal):
    return bool(
        world.options.objective == goal
        or goal == VOTVGoal.KERFUR_OMEGA and world.options.kerfur_omega_enabled.value
        or goal == VOTVGoal.HELL_ROCK and world.options.hell_rock_enabled.value
        or goal == VOTVGoal.WHITE_ARGEMIA_PLUSH
        or goal == VOTVGoal.LAMBERT_PLUSH and world.options.lambert_plush_enabled.value
        or goal == VOTVGoal.GREEN_CABINET and world.options.green_cabinet_enabled.value
    )

def furfur_plush_enabled(world: "VOTVWorld"):
    return bool(world.options.buried_items.value and world.options.time_sensitive.value)

def day_item_count(world: "VOTVWorld"):
    return (
        world.options.survive_day.value if world.options.objective == VOTVGoal.SURVIVE else max(
            world.options.survive_days_locations.value,
            7 if world.options.time_sensitive.value else 0,  # Green Fire Rock is only obtainable on Day 8+
            1 if world.options.daily_task_locations.value else 0
        )
    )

@dataclass(frozen=True)
class DayItemFieldResolver(FieldResolver, game="Voices of the Void"):
    count: int
    """The expected amount of day items necessary. If there are less than that amount in the multiworld, checks if all of them have been gotten."""

    @override
    def resolve(self, world: "VOTVWorld") -> Any:
        return min(self.count, day_item_count(world))
