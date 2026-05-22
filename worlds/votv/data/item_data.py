from functools import reduce
from typing import TYPE_CHECKING, Callable, NamedTuple, Optional
from BaseClasses import ItemClassification as IC

from ..Options import ATVUpgradesAsItems, ArgemiaPlushes, PhysicalModulesAsItems, UpgradesAsItems
from ..Utils import furfur_plush_enabled, is_goal_enabled, resolve
from ..Types import VOTVGoal

if TYPE_CHECKING:
    from .. import VOTVWorld

class ShopItem(NamedTuple):
    cost: Optional[int] = 1
    size: Optional[int] = 1
    internal_name: Optional[str] = ""
    classification: IC = IC.filler
    unlock: Optional[list[str] | str] = ""

    def checkUnlock(self, whitelist: list[str]):
        if self.unlock != "":
            unlocks = []
            if type(self.unlock) == list:
                unlocks = self.unlock
            else:
                unlocks = [self.unlock]
            if not all(rule in whitelist for rule in unlocks):
                return False
        return True

#my general classifications are
#things you actually need to do your job = useful
#help you do anything remotely helpful = useful
#logic = progression
#anything else = filler
#containers i think should be classified as useful only because if they arent in the shop
#youre kinda screwed on putting stuff up lol
shop_items = {
    "Drive":                            ShopItem(2, 1, "drive", IC.useful),
    "Drive box":                        ShopItem(5, 5, "box_p", IC.useful),
    "Burger":                           ShopItem(90, 1, "burger", IC.filler),
    "Food box":                         ShopItem(15, 1, "foodbox", IC.filler),
    "MRE":                              ShopItem(50, 1, "mre", IC.useful),
    # "Shrimps pack":                     ShopItem(35, 1, "shrimp", IC.filler),
    "Coffee chocolate bar":             ShopItem(30, 1, "choco", IC.filler),
    "Cup":                              ShopItem(1, 1, "cup", IC.filler),
    "Coffee bag":                       ShopItem(50, 1, "coffee_b", IC.filler),
    "Battery":                          ShopItem(45, 1, "batts", IC.useful),
    "Gas can":                          ShopItem(50, 1, "gascan", IC.useful),
    "Coffee machine":                   ShopItem(200, 1, "coffee_m", IC.filler),
    "Clocks":                           ShopItem(35, 1, "clocks", IC.filler),
    "Curtains":                         ShopItem(20, 20, "curtains", IC.filler),
    "Wooden pallet":                    ShopItem(20, 20, "palete", IC.filler),
    "Cacti":                            ShopItem(20, 1, "reginald", IC.filler),
    "Vase":                             ShopItem(50, 5, "vase", IC.filler),
    # "Crowbar":                          ShopItem(50, 1, "crowbar", IC.useful),
    "Soccer ball":                      ShopItem(25, 1, "soccer", IC.filler),
    # "Camera [Bad]":                     ShopItem(20, 1, "cam_h_0", IC.filler),
    # "Camera [Med]":                     ShopItem(50, 1, "cam_h_1", IC.filler),
    #Progression for Kerfuro
    # "Camera [Good]":                    ShopItem(120, 1, "cam_h_2", IC.progression),
    #
    "Pot (empty)":                      ShopItem(15, 10, "pot", IC.filler),
    "Pot plant (bush) 1":               ShopItem(20, 10, "pot_0", IC.filler),
    "Pot plant (big cactus)":           ShopItem(35, 10, "pot_1", IC.filler),
    "Pot plant (bush) 2":               ShopItem(35, 10, "pot_2", IC.filler),
    "Pot plant (bush) 3":               ShopItem(35, 10, "pot_3", IC.filler),
    "Pot plant (bush) 4":               ShopItem(35, 10, "pot_4", IC.filler),
    "Pot plant (bush) 5":               ShopItem(35, 10, "pot_5", IC.filler),
    "Pot plant (bush) 6":               ShopItem(35, 10, "pot_6", IC.filler),
    "Pot plant (bush) 7":               ShopItem(35, 10, "pot_7", IC.filler),
    "Pot plant (bush) 8":               ShopItem(35, 10, "pot_8", IC.filler),
    "Pot plant (bush) 9":               ShopItem(35, 10, "pot_9", IC.filler),
    "Pot plant (bush) 10":              ShopItem(35, 10, "pot_10", IC.filler),
    "Pot plant (bush) 11":              ShopItem(35, 10, "pot_12", IC.filler),
    "Pot plant (bush) 12":              ShopItem(35, 10, "pot_15", IC.filler),
    "Pot plant (bush) 13":              ShopItem(35, 10, "pot_16", IC.filler),
    "Pot plant (bush) 14":              ShopItem(35, 10, "pot_17", IC.filler),
    "Barrel":                           ShopItem(80, 25, "barrel", IC.useful),
    "Crate":                            ShopItem(50, 20, "crate", IC.useful),
    "Wooden chair":                     ShopItem(30, 10, "chair", IC.filler),
    # "Digital map":                      ShopItem(150, 1, "Map", IC.useful),
    "Sponge":                           ShopItem(3, 1, "sponge", IC.filler),
    "Soap":                             ShopItem(5, 1, "soap", IC.filler),
    "Bucket":                           ShopItem(30, 1, "bucket", IC.filler),
    "Cake (not a lie)":                 ShopItem(60, 1, "cake", IC.filler),
    "Cookie":                           ShopItem(1, 1, "cookie", IC.filler),
    "Notepad":                          ShopItem(12, 1, "clipboard", IC.filler),
    "Paper sheet":                      ShopItem(1, 1, "paper", IC.filler),
    "Woodchipper":                      ShopItem(250, 50, "woodchipper", IC.filler),
    "Pet rock":                         ShopItem(35, 1, "petrock", IC.filler),
    "Rock":                             ShopItem(15, 1, "rock", IC.filler),
    "Beacon":                           ShopItem(40, 1, "beacon", IC.filler),
    "Rug (Rectangle Blue)":             ShopItem(50, 1, "rug_0", IC.filler),
    "Rug (Rectangle Red)":              ShopItem(50, 1, "rug_1", IC.filler),
    "Rug (Rectangle Green)":            ShopItem(50, 1, "rug_2", IC.filler),
    "Rug (Rectangle Gray)":             ShopItem(50, 1, "rug_3", IC.filler),
    "Rug (Round Gray)":                 ShopItem(50, 1, "rug_4", IC.filler),
    "Rug (Round Brown)":                ShopItem(50, 1, "rug_5", IC.filler),
    "Rug (Round White)":                ShopItem(50, 1, "rug_6", IC.filler),
    "Rug (Round Blue)":                 ShopItem(50, 1, "rug_7", IC.filler),
    "Rug (Square White)":               ShopItem(50, 1, "rug_8", IC.filler),
    "Rug (Square Red)":                 ShopItem(50, 1, "rug_9", IC.filler),
    "Rug (Square Gray)":                ShopItem(50, 1, "rug_10", IC.filler),
    "Rug (Square Brown)":               ShopItem(50, 1, "rug_11", IC.filler),
    "Rug (Long Red)":                   ShopItem(50, 1, "rug_12", IC.filler),
    "Rug (Custom)":                     ShopItem(60, 1, "rug_c", IC.filler),
    # "Backpack":                         ShopItem(150, 50, "backpack", IC.useful),
    "Broomba":                          ShopItem(100, 1, "roomba", IC.filler),
    "Spotlight (tripod)":               ShopItem(150, 50, "spotlight_b", IC.filler),
    "Spotlight (head)":                 ShopItem(300, 50, "spotlight_h", IC.filler),
    "cool funy sweden man (real) (no fake)": ShopItem(69, 1, "varg", IC.filler),
    "cool funy ctuhu man (real) (no fake)": ShopItem(69, 1, "igp", IC.filler),
    "cool funy banana moth (real) (no fake)": ShopItem(69, 1, "bananMoth", IC.filler),
    # "Toolbox":                          ShopItem(100, 1, "toolbox", IC.filler),
    "Glowstick (white)":                ShopItem(30, 1, "glowstick", IC.filler),
    "Glowstick (red)":                  ShopItem(30, 1, "glowstick_R", IC.filler),
    "Glowstick (green)":                ShopItem(30, 1, "glowstick_G", IC.filler),
    "Glowstick (blue)":                 ShopItem(30, 1, "glowstick_B", IC.filler),
    "Glowstick (cyan)":                 ShopItem(30, 1, "glowstick_C", IC.filler),
    "Glowstick (yellow)":               ShopItem(30, 1, "glowstick_Y", IC.filler),
    "Glowstick (magenta)":              ShopItem(30, 1, "glowstick_M", IC.filler),
    "Sleeping bag":                     ShopItem(150, 25, "sleepingbag", IC.filler),
    #Custom content
    "Picture (horizontal)":             ShopItem(15, 1, "pic_h", IC.filler, "custom"),
    "Picture (square)":                 ShopItem(15, 1, "pic_s", IC.filler, "custom"),
    "Picture (vertical)":               ShopItem(15, 1, "pic_v", IC.filler, "custom"),
    "Picture (table)":                  ShopItem(15, 1, "pic_t", IC.filler, "custom"),
    #
    "Remote drone":                     ShopItem(300, 1, "Rdrone", IC.filler),
    "Arcade machine":                   ShopItem(200, 50, "arcade_inv", IC.filler),
    "Syrup bottle":                     ShopItem(13, 1, "pills_bt_1", IC.useful),
    "Pills bottle":                     ShopItem(22, 1, "pills_bt_0", IC.useful),
    "Pills box":                        ShopItem(35, 1, "pills_b", IC.useful),
    "Sleep pills":                      ShopItem(100, 1, "sleeppills", IC.useful),
    "Heavy meds":                       ShopItem(250, 1, "cancerMeds", IC.useful),
    # "First aid medkit":                 ShopItem(75, 1, "medkit", IC.useful),
    "Shelf":                            ShopItem(20, 50, "shelf", IC.filler),
    "Pizza":                            ShopItem(125, 1, "pizza", IC.filler),
    "Pizza (Pineapple)":                ShopItem(125, 1, "pizza_0", IC.filler),
    "Pizza (Mushrooms)":                ShopItem(125, 1, "pizza_1", IC.filler),
    "Pizza (Shrimp)":                   ShopItem(125, 1, "pizza_2", IC.filler),
    "Taco":                             ShopItem(20, 1, "taco", IC.filler),
    "meatball":                         ShopItem(500, 50, "meatball", IC.filler),
    "Toblerone":                        ShopItem(15, 1, "toblerone", IC.filler),
    "Basketball hoop":                  ShopItem(60, 1, "basketHoop", IC.filler),
    "Drive rack":                       ShopItem(50, 1, "driveRack", IC.useful),
    "Pumpkin":                          ShopItem(50, 1, "pumpkin", IC.filler),
    "\"Zeta Reticulan\" alien figure":  ShopItem(100, 1, "grayFigure_s", IC.filler),
    #progression for kerfuro
    # "\"Kerfur\" blue":                  ShopItem(500, 25, "kerfus", IC.progression),
    # "\"Kerfur\" pink":                  ShopItem(500, 25, "kerfus_0", IC.progression),
    # "\"Kerfur\" red":                   ShopItem(500, 25, "kerfus_1", IC.progression),
    #after completing Abandoned Kerfur
    # "\"Kerfur\" orange++":              ShopItem(400, 25, "kerfus_2", IC.useful, "murderfur"),
    #
    "Digital camera":                   ShopItem(100, 1, "digcam", IC.filler),
    # "Hook":                             ShopItem(50, 1, "hook", IC.useful),
    # "Metal detector":                   ShopItem(300, 1, "mdetect", IC.useful),
    # "Balloon pack (WIP)":               ShopItem(100, 1, "balloonP", IC.filler),
    "Bedside table":                    ShopItem(60, 10, "bedtable", IC.useful),
    "Password changer":                 ShopItem(200, 1, "passchange", IC.filler),
    "Chicken nugget":                   ShopItem(3, 1, "chnugg", IC.filler),
    "Hammer (WIP)":                     ShopItem(50, 1, "hammer", IC.filler),
    "Wooden plank":                     ShopItem(20, 10, "plank", IC.filler),
    "Curtains (chromakey)":             ShopItem(10, 10, "curtains_0", IC.filler),
    "Roach repellent":                  ShopItem(150, 1, "roachRepel", IC.filler),
    "Disc box":                         ShopItem(60, 1, "discBox", IC.filler),
    "Metal sheet":                      ShopItem(10, 1, "metalSheet", IC.filler),
    #custom content
    "Flag (small)":                     ShopItem(15, 1, "flag_S", IC.filler, "custom"),
    "Flag (medium)":                    ShopItem(25, 10, "flag_M", IC.filler, "custom"),
    "Flag (large)":                     ShopItem(35, 5, "flag_L", IC.filler, "custom"),
    #
    "Traffic cone":                     ShopItem(20, 5, "cone", IC.filler),
    "\"Wet floor\" sign":               ShopItem(15, 5, "wfloor", IC.filler),
    "Desk lamp":                        ShopItem(200, 5, "deskLamp", IC.filler),
    # "Lighter":                          ShopItem(100, 1, "ligther", IC.filler),
    #Custom content
    "TV":                               ShopItem(150, 10, "tv_0", IC.filler, "custom"),
    "Radio":                            ShopItem(80, 10, "radio_o", IC.filler, "custom"),
    #
    "Couch (small)":                    ShopItem(50, 30, "couch_0", IC.filler),
    "Couch (big)":                      ShopItem(70, 40, "couch_1", IC.filler),
    "Fire extinguisher":                ShopItem(50, 5, "fireExt", IC.filler),
    "Nail":                             ShopItem(3, 1, "nail", IC.filler),
    "Axle Nail":                        ShopItem(4, 1, "nail_ax", IC.filler),
    "Toilet paper roll":                ShopItem(10, 1, "toiletroll", IC.filler),
    "Bun":                              ShopItem(30, 1, "bun_0", IC.filler),
    "Small pot (empty)":                ShopItem(10, 5, "pot_s", IC.filler),
    "Pot flower (red)":                 ShopItem(20, 5, "pot_s_0", IC.filler),
    "Pot flower (purple)":              ShopItem(20, 5, "pot_s_1", IC.filler),
    "Pot flower (small red)":           ShopItem(20, 5, "pot_s_2", IC.filler),
    "Pot flower (white)":               ShopItem(20, 5, "pot_s_3", IC.filler),
    "Pot flower (yellow)":              ShopItem(20, 10, "pot_s_4", IC.filler),
    "Pot flower (grass) 1":             ShopItem(20, 5, "pot_s_5", IC.filler),
    "Pot flower (grass) 2":             ShopItem(20, 5, "pot_s_6", IC.filler),
    "Pot flower (grass) 3":             ShopItem(20, 5, "pot_s_7", IC.filler),
    "Item box":                         ShopItem(10, 50, "drivebox_b", IC.useful),
    "Banana":                           ShopItem(10, 1, "banana", IC.filler),
    # "Hazmat suit":                      ShopItem(300, 1, "hazsuit", IC.filler),
    #custom content
    "Industrial 3D printer":            ShopItem(150, 50, "printer", IC.filler, "custom"),
    "Sticker pack (WIP)":               ShopItem(100, 1, "stickers", IC.filler, "custom"),
    "Custom poster":                    ShopItem(25, 1, "poster_c", IC.filler, "custom"),
    #
    "Mannequin":                        ShopItem(50, 1, "mann1", IC.filler),
    "Cardboard box (2x2x2)":            ShopItem(15, 2, "cbox_222", IC.useful),
    "Cardboard box (4x2x2)":            ShopItem(30, 4, "cbox_422", IC.useful),
    "Cardboard box (4x4x2)":            ShopItem(50, 8, "cbox_442", IC.useful),
    "Cardboard box (4x4x4)":            ShopItem(100, 16, "cbox_444", IC.useful),
    "Cardboard box (8x4x4)":            ShopItem(150, 32, "cbox_844", IC.useful),
    "Cardboard box (8x8x4)":            ShopItem(200, 32, "cbox_884", IC.useful),
    "Cardboard box (8x8x8)":            ShopItem(300, 32, "cbox_888", IC.useful),
    #custom content?
    "Fax/printer (WIP)":                ShopItem(500, 20, "fax", IC.filler),
    #
    "Thermometer (WIP)":                ShopItem(100, 1, "thermometer", IC.filler),
    "Microwave":                        ShopItem(400, 40, "microwave_0", IC.filler),
    "Popcorn bag":                      ShopItem(20, 1, "popcorn", IC.filler),
    "Cork board":                       ShopItem(75, 50, "corkboard", IC.filler),
    "Ball of red string":               ShopItem(55, 1, "rope", IC.filler),
    "Pencil":                           ShopItem(20, 1, "pencil", IC.filler),
    "\"Meter\" ruler":                  ShopItem(20, 5, "meter", IC.filler),
    "Measuring tape":                   ShopItem(200, 5, "ruler", IC.filler),
    "Garbage bag":                      ShopItem(1, 1, "garbBag_f", IC.filler),
    "Garbage bag roll":                 ShopItem(16, 1, "garbBag_r", IC.filler),
    "Ultrabait box \"Lure\"":           ShopItem(200, 1, "ubaitBox_1", IC.filler),
    "Ultrabait box \"Luck\"":           ShopItem(250, 1, "ubaitBox_0", IC.filler),
    "Ultrabait box \"No-bite\"":        ShopItem(350, 1, "ubaitBox_2", IC.filler),
    "Ultrabait box \"Ultimate\"":       ShopItem(600, 1, "ubaitBox_3", IC.filler),
    "Mop":                              ShopItem(300, 25, "mop", IC.filler),
    "Mop bucket":                       ShopItem(60, 25, "mop_b", IC.filler),
    "Broom":                            ShopItem(50, 25, "broom", IC.filler),
    "Farm pot":                         ShopItem(75, 25, "fpot", IC.filler),
    "Metal table 1":                    ShopItem(75, 25, "table_1", IC.filler),
    "Metal table 2":                    ShopItem(75, 25, "table_2", IC.filler),
    "Coffee table":                     ShopItem(40, 20, "coffeTable", IC.filler),
    "Workbench":                        ShopItem(200, 1, "workbench", IC.filler),
    "Metal chair":                      ShopItem(40, 10, "chairfold", IC.filler),
    "Pin box":                          ShopItem(75, 1, "pinbox", IC.filler),
    "Cheese":                           ShopItem(30, 1, "cheese", IC.filler),
    "Wall shelf":                       ShopItem(40, 1, "wlshelf_0", IC.filler),
    "Salt lamp":                        ShopItem(150, 10, "saltLamp", IC.filler),
    "Kallaks 1x1":                      ShopItem(20, 10, "wshelf_0", IC.filler),
    "Kallaks 2x1":                      ShopItem(30, 20, "wshelf_1", IC.filler),
    "Kallaks 4x1":                      ShopItem(55, 30, "wshelf_2", IC.filler),
    "Kallaks 4x1":                      ShopItem(100, 40, "wshelf_3", IC.filler),
    "Can opener":                       ShopItem(100, 1, "canopener", IC.filler),
    "Kitchen knife":                    ShopItem(50, 1, "ut_knife", IC.filler),
    "Portable hot plate":               ShopItem(350, 1, "cookingPad", IC.filler),
    "Battery charger":                  ShopItem(400, 1, "batteryCharger", IC.filler),
    "Accumulator battery":              ShopItem(150, 1, "batt_a", IC.filler),
    "Plate small (open container)":     ShopItem(25, 1, "plate_oc_S", IC.filler),
    "Plate large (open container)":     ShopItem(30, 1, "plate_oc_L", IC.filler),
    "Bowl small (open container)":      ShopItem(20, 1, "bowl_oc_S", IC.filler),
    "Bowl medium (open container)":     ShopItem(25, 1, "bowl_oc_M", IC.filler),
    "Bowl larger (open container)":     ShopItem(30, 1, "bowl_oc_L", IC.filler),
    #Custom content
    "Plasma tv":                        ShopItem(450, 30, "plasmaTv", IC.filler, "custom"),
    #
    "Bedside table":                    ShopItem(50, 50, "wf_bedtable", IC.filler),
    "Bookshelf":                        ShopItem(150, 50, "wf_bshelf", IC.filler),
    "Drawer":                           ShopItem(150, 50, "wf_drawer", IC.filler),
    "Wardrobe":                         ShopItem(250, 50, "wf_wardrobe", IC.filler),
    "Minifridge":                       ShopItem(400, 50, "minifridge", IC.filler),
    "Wall builder (WIP)":               ShopItem(500, 1, "wallbuilder", IC.filler),
    "Brick stack":                      ShopItem(40, 1, "brickStack", IC.filler),
    "Wall fixer (WIP)":                 ShopItem(100, 1, "wallfixer", IC.filler),
    "GPU board":                        ShopItem(200, 1, "miner_gpu", IC.useful),
    "Frame":                            ShopItem(200, 50, "miner", IC.useful),
    "Swatter":                          ShopItem(100, 1, "swatter", IC.filler),
    "Nailgun":                          ShopItem(300, 1, "nailgun", IC.filler),
    "Sell gun":                         ShopItem(2000, 1, "coingun", IC.filler),
    "Wall light (small)":               ShopItem(75, 1, "lightl_2", IC.filler),
    "Wall light (big)":                 ShopItem(125, 1, "lightl_3", IC.filler),
    "cool funy glass cat (real) (no fake)": ShopItem(69, 1, "3cat", IC.filler),
    "Floor lamp":                       ShopItem(150, 1, "floorlamp", IC.filler),
    "Wooden table (Small)":             ShopItem(50, 20, "dtable_0", IC.filler),
    "Wooden table (Medium)":            ShopItem(100, 40, "dtable_1", IC.filler),
    "Wooden table (Large)":             ShopItem(150, 50, "dtable_2", IC.filler),
    "Wooden chair":                     ShopItem(50, 15, "dchair", IC.filler),
    "Bread":                            ShopItem(35, 1, "bread", IC.filler),
    "Cucumber":                         ShopItem(15, 1, "cucumber", IC.filler),
    "Lemon":                            ShopItem(35, 1, "lemon", IC.filler),
    "Mango":                            ShopItem(40, 1, "mango", IC.filler),
    "Orange":                           ShopItem(25, 1, "orange", IC.filler),
    "Pineapple":                        ShopItem(40, 1, "pineapple", IC.filler),
    "Tomato":                           ShopItem(20, 1, "tomato", IC.filler),
    "Watermelon":                       ShopItem(50, 1, "watermelon", IC.filler),
    "Portable pressure washer":         ShopItem(500, 50, "rifle_4", IC.filler),
    "Ramp":                             ShopItem(60, 1, "ramp", IC.filler),
    "BBQ grill":                        ShopItem(300, 1, "bbq", IC.filler),
    "BBQ grill lid":                    ShopItem(30, 1, "bbq_1", IC.filler),
    "Plastic garden chair":             ShopItem(20, 15, "gplasticChair", IC.filler),
    "Wooden garden chair":              ShopItem(35, 15, "gwoodenChair", IC.filler),
    #custom content
    "Medium TV":                        ShopItem(300, 25, "floortv_s", IC.filler, "custom"),
    #
    "Wooden garden table":              ShopItem(75, 40, "gwoodenTable", IC.filler),
    "Beer":                             ShopItem(20, 1, "beer_c", IC.filler),
    # "Scuba mask":                       ShopItem(200, 1, "scuba", IC.filler),
    # "Scuba mask tank":                  ShopItem(400, 1, "scuba_t", IC.filler),
    # "Bike helmet":                      ShopItem(1000, 1, "bikehelmet", IC.useful),
    "Cig pack":                         ShopItem(100, 1, "cigp", IC.filler),
    "Baguette":                         ShopItem(40, 1, "french", IC.filler),
    "Giant \"Keljoy\" plush":           ShopItem(800, 50, "kelplush_0", IC.filler),
    "Fire protection suit":             ShopItem(600, 1, "firesuit", IC.filler),
    "Wastebasket":                      ShopItem(20, 1, "wastebasket", IC.filler),
    "Plastic crate (open container)":   ShopItem(30, 1, "beercrate_oc", IC.filler),
    "Plunger":                          ShopItem(25, 5, "plunger", IC.filler),
    # "Car keys":                         ShopItem(150, 1, "carKeys", IC.filler),
    "Alarm clock":                      ShopItem(200, 1, "tableclocks", IC.filler),
    "Wall clocks":                      ShopItem(100, 1, "wallclocks", IC.filler),
    "TV remote":                        ShopItem(100, 1, "tvremote", IC.filler),
    "Neon sign (ASO)":                  ShopItem(350, 40, "neon_0", IC.filler),
    "Neon sign (Erie Zone)":            ShopItem(300, 40, "neon_1", IC.filler),
    "Neon sign (Keljoy)":               ShopItem(200, 40, "neon_2", IC.filler),
    "Neon sign (Kerfur)":               ShopItem(200, 40, "neon_3", IC.filler),
    "Neon sign (Monique)":              ShopItem(250, 40, "neon_4", IC.filler),
    "Neon sign (Stolas)":               ShopItem(300, 40, "neon_5", IC.filler),
    "Neon sign (Erie Cafe)":            ShopItem(350, 40, "neon_6", IC.filler),
    "Neon sign (Erie's Cove)":          ShopItem(500, 50, "neon_7", IC.filler),
    "Neon sign (Vinesauce)":            ShopItem(300, 40, "neon_8", IC.filler),
    "Cool funny party demon":           ShopItem(69, 1, "partydemon", IC.filler),
    "Cigar":                            ShopItem(500, 1, "cigar", IC.filler),
    "Ashtray":                          ShopItem(40, 1, "ashtray", IC.filler),
    "AGL rocket":                       ShopItem(300, 1, "saltrocket", IC.filler),
    #unlocked after Upgrade
    # "Omega AI module":                  ShopItem(300, 1, "kerfsp_0", IC.filler, "kerfuro"),
    # "Ball joint":                       ShopItem(25, 1, "kerfsp_1", IC.filler, "kerfuro"),
    # "Limb joint":                       ShopItem(20, 1, "kerfsp_2", IC.filler, "kerfuro"),

    "Glue bottle":                      ShopItem(50, 1, "glue_0", IC.filler),
    "Trampoline":                       ShopItem(400, 50, "trampoline", IC.filler),
    # "Hacksaw":                          ShopItem(300, 1, "hacksaw", IC.useful),
    "Hotdog":                           ShopItem(80, 1, "hotdog", IC.filler),
    "Steak (raw)":                      ShopItem(80, 1, "steak_r", IC.filler),
    "Flour bag":                        ShopItem(35, 1, "flour", IC.filler),
    "Fanny pack":                       ShopItem(500, 1, "fannypack", IC.filler),
    "Scrap box (open container)":       ShopItem(55, 20, "scrapbox", IC.filler),
    "Wooden cutting board":             ShopItem(50, 1, "cuttingboard", IC.filler),
    # "Cooking book":                     ShopItem(100, 1, "cookingbook", IC.filler),
    "Compass":                          ShopItem(90, 1, "compass", IC.filler),
    "Flashlight":                       ShopItem(70, 1, "flashlight", IC.filler),
    "Glasses":                          ShopItem(50, 1, "glasses", IC.filler),
    "Rake":                             ShopItem(500, 1, "rake", IC.filler),
    "Antique":                          ShopItem(400, 1, "watches", IC.filler),
    "Garden hose":                      ShopItem(50, 10, "hose", IC.filler),
    "Water sprinkler":                  ShopItem(200, 10, "sprinkler", IC.filler),
    "Faucet":                           ShopItem(100, 10, "faucet", IC.filler),
    "Printer camera":                   ShopItem(600, 1, "printcam", IC.filler),
    "Blueprint (EMF equipment)":        ShopItem(300, 1, "blueprint_emf", IC.filler),
    "Blueprint (Geiger equipment)":     ShopItem(400, 1, "blueprint_geiger", IC.filler),
    "Small globe":                      ShopItem(60, 1, "globeS", IC.filler),
    "Large globe":                      ShopItem(250, 1, "globeL", IC.filler),
    "Rolling pin":                      ShopItem(45, 1, "rollingpin", IC.filler),
    "Bread mold":                       ShopItem(50, 1, "breadMold", IC.filler),
    "Compost bucket":                   ShopItem(100, 1, "compostB", IC.filler),
    "Blueprint (Bee box)":              ShopItem(200, 1, "blueprint_beebox", IC.filler),
    "Baking tray":                      ShopItem(45, 1, "bakingtray", IC.filler),
    #christmas event
    "Butter churn":                     ShopItem(120, 1, "butter_c", IC.filler, "christmas"),
    #
    "Milk bottle":                      ShopItem(50, 1, "milk_n", IC.filler),
    #christmas event
    "Torch":                            ShopItem(40, 1, "torch", IC.filler, "christmas"),
    "Torch holder":                     ShopItem(35, 1, "torch_h", IC.filler, "christmas"),
    "Wool boot":                        ShopItem(40, 1, "woolboot", IC.filler, "christmas"),
    "Tio de Nadal":                     ShopItem(500, 1, "shitlog", IC.filler, "christmas"),
    "Thorn wreath":                     ShopItem(30, 1, "tWreath", IC.filler, "christmas"),
    "Christmas decoration (wreath)":    ShopItem(20, 1, "cw_wreath", IC.filler, "christmas"),
    "Christmas decoration (two candles in a wreath)": ShopItem(25, 1, "cw_2candle", IC.filler, "christmas"),
    "Christmas decoration (three candles)": ShopItem(30, 1, "cw_3candle", IC.filler, "christmas"),
    "Christmas decoration (three candles in a wreath)": ShopItem(35, 1, "cw_full", IC.filler, "christmas"),
    #
    "Blueprint (Portable metal detector)": ShopItem(350, 1, "blueprint_metaldetec", IC.filler),
    #christmas event
    "Christmas lights":                 ShopItem(100, 1, "xmaslights", IC.filler, "christmas"),
    "Christmas lights (no light)":      ShopItem(100, 1, "xmaslights_0", IC.filler, "christmas"),
    ##must pacify krampus with The Brew
    "Krampus hat":                      ShopItem(200, 1, "krampushat", IC.filler, ["christmas", "krampus"]),
    ##
    "pigeon":                           ShopItem(100, 0, "pigeon", IC.filler, "christmas"),
    #
    "Clean jar":                        ShopItem(25, 1, "cleanJar", IC.filler),
    "Sugar bag":                        ShopItem(250, 1, "sugar", IC.filler),
    "Crank flashlight":                 ShopItem(400, 1, "flashlight_c", IC.filler),
    "Mittens":                          ShopItem(100, 1, "mittens", IC.filler),
    #custom content
    "Desktop 3D printer":               ShopItem(400, 25, "printer_d", IC.filler, "custom"),
    #
    "Cardboard box":                    ShopItem(20, 10, "cardbbox", IC.filler),
    "Smoke detector box":               ShopItem(100, 1, "smokedetec", IC.filler),
    #must dig up first
    # "Maid outfit":                      ShopItem(250, 1, "kerfoout_maid", IC.filler | EC.funny, "maid"),
    "Bandage":                          ShopItem(35, 1, "bandage", IC.filler),
}

if TYPE_CHECKING:
    Classification = dict[IC, int]
    DynamicClassification = Callable[[VOTVWorld], dict[IC, int]]
    ClassificationResolvable = dict[IC, int] | DynamicClassification

class ExtraItem(NamedTuple):
    classification: ClassificationResolvable

def goal_item(goals: set[VOTVGoal], classification: ClassificationResolvable) -> DynamicClassification:
    def resolve_goal_item(world: VOTVWorld):
        # The item's objective is active: override all other filters and set all classification to progression
        if world.options.objective.value in goals:
            copy = world.options.as_dict()
            world.options.argemia_plushes.value = ArgemiaPlushes.option_all
            world.options.buried_items.value = 1
            world.options.time_sensitive.value = 1
            world.options.scrap_recipes_as_items.value = 1
            world.options.funny_setting.value = 1
            world.options.upgrades_as_items.value = UpgradesAsItems.option_all
            world.options.physical_modules_as_items.value = PhysicalModulesAsItems.option_all
            world.options.atv_upgrades_as_items.value = ATVUpgradesAsItems.option_all

            result = resolve(plus(*({IC.progression: v} for v in classification.values())), world)

            world.options.argemia_plushes.value = copy["argemia_plushes"]
            world.options.buried_items.value = copy["buried_items"]
            world.options.time_sensitive.value = copy["buried_items"]
            world.options.scrap_recipes_as_items.value = copy["scrap_recipes_as_items"]
            world.options.funny_setting.value = copy["funny_setting"]
            world.options.upgrades_as_items.value = copy["upgrades_as_items"]
            world.options.physical_modules_as_items.value = copy["physical_modules_as_items"]
            world.options.atv_upgrades_as_items.value = copy["atv_upgrades_as_items"]

            return result

        if any(is_goal_enabled(world, x) for x in goals):
            return resolve(classification, world)
        
        return {}

    return resolve_goal_item

def argemia_plush(setting: int, classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: resolve(classification, world) if world.options.argemia_plushes.value >= setting else {}

def buried(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: resolve(classification, world) if world.options.buried_items.value else {}

def time_sensitive(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: resolve(classification, world) if world.options.time_sensitive.value else {}

def recipe(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: resolve(classification, world) if world.options.scrap_recipes_as_items.value else {}

def funny(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: resolve(classification, world) if world.options.funny_setting.value else {}

def upgrade(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: {k: v for k, v in resolve(classification, world).items() if world.options.upgrades_as_items.value == UpgradesAsItems.option_all or world.options.upgrades_as_items.value == UpgradesAsItems.option_useful and (k & IC.progression or k & IC.useful)}

def module(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: {k: v for k, v in resolve(classification, world).items() if world.options.physical_modules_as_items.value == PhysicalModulesAsItems.option_all or world.options.physical_modules_as_items.value == PhysicalModulesAsItems.option_useful and (k & IC.progression or k & IC.useful)}

def atv_upgrade(classification: ClassificationResolvable) -> DynamicClassification:
    return lambda world: {k: v for k, v in resolve(classification, world).items() if world.options.atv_upgrades_as_items.value == ATVUpgradesAsItems.option_all or world.options.atv_upgrades_as_items.value == ATVUpgradesAsItems.option_useful and (k & IC.progression or k & IC.useful)}

def plus(*args: ClassificationResolvable) -> DynamicClassification:
    return lambda world: {
        k: sum(resolve(x, world)[k] if k in resolve(x, world) else 0 for x in args)
        for k in reduce(lambda acc, x: {*acc, *resolve(x, world).keys()}, args, set())
    }

goal_items = {
    "Metal Detector":                   ExtraItem(lambda world: {IC.progression: 1} if world.options.buried_items.value else goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})(world)),
    "Kerfur-Omega Complete Manual":     ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 1})),
    "Red Kerfur":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Blue Kerfur":                      ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Pink Kerfur":                      ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Omega AI Module":                  ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 1})),
    "Ball Joint":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, buried({IC.filler: 12}))),
    "Limb Joint":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 6})),
    "Progressive Camera":               ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 3})),
    "Hacksaw":                          ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Pickaxe":                          ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.useful: 1})),
    "Hazmat Suit":                      ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 1})),
    "Gas Welder":                       ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 3})),
    "Radioactive Capsule Blueprint":    ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 1})),
    "Radioactive Capsule":              ExtraItem(goal_item({VOTVGoal.KERFUR_OMEGA}, {IC.filler: 1})),

    "Skull":                            ExtraItem(goal_item({VOTVGoal.HELL_ROCK, VOTVGoal.BLACK_ARGEMIA_PLUSH}, plus({IC.filler: 5}, buried({IC.filler: 2})))),

    "Red Argemia Plush":                ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgb, {IC.filler: 1}))),
    "Blue Argemia Plush":               ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgb, {IC.filler: 1}))),
    "Green Argemia Plush":              ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgb, {IC.filler: 1}))),
    "Yellow Argemia Plush":             ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.filler: 1}))),
    "Magenta Argemia Plush":            ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.filler: 1}))),
    "Cyan Argemia Plush":               ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, argemia_plush(ArgemiaPlushes.option_rgbycm, {IC.filler: 1}))),
    "Shrimp Pack":                      ExtraItem(goal_item({VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}, {IC.useful: 17})),

    "Balloon Pack (WIP)":               ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Fire Rune":                        ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Earth Rune":                       ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Water Rune":                       ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Air Rune":                         ExtraItem(goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})),
    "Ritual Knife":                     ExtraItem(lambda world: {IC.progression: 1} if furfur_plush_enabled(world) else goal_item({VOTVGoal.LAMBERT_PLUSH}, {IC.filler: 1})(world)),

    "Tile":                             ExtraItem(goal_item({VOTVGoal.GREEN_CABINET}, {IC.filler: 9}))
}

extra_items = {
    "Half Hook":                                        ExtraItem({IC.progression: 1, IC.useful: 1}),
    "Shovel":                                           ExtraItem({IC.progression: 1, IC.useful: 3}),
    "Bunker Keycard":                                   ExtraItem({IC.progression: 1}),
    "Scuba Mask":                                       ExtraItem({IC.progression: 1}),
    "Scuba Mask Tank":                                  ExtraItem({IC.progression: 1}),
    "Metal Scrap Recipe":                               ExtraItem(recipe({IC.progression: 1})),
    "Electronic Scrap Recipe":                          ExtraItem(recipe({IC.progression: 1})),
    "Glass Scrap Recipe":                               ExtraItem(recipe({IC.progression: 1})),
    "Plastic Scrap Recipe":                             ExtraItem(recipe({IC.progression: 1})),
    "Progressive Processing Level":                     ExtraItem(upgrade({IC.progression: 3})),
    "Lifecrystal Signal":                               ExtraItem(lambda world: {IC.progression: 1} if any(is_goal_enabled(world, x) for x in {VOTVGoal.HELL_ROCK, VOTVGoal.WHITE_ARGEMIA_PLUSH, VOTVGoal.BLACK_ARGEMIA_PLUSH}) else {}),
    "Hiking Boots":                                     ExtraItem({IC.progression: 1}),
    "Lighter":                                          ExtraItem({IC.progression: 1}),
    "Cig Pack":                                         ExtraItem({IC.progression: 1}),
    "Crowbar":                                          ExtraItem(lambda world: {(IC.progression if world.options.chicken_sandwiches.value else IC.useful): 1}),
    "Day":                                              ExtraItem(lambda world: {IC.progression: 50} if world.options.day_as_items.value else {}),

    "Furfur Altar Leg 1":                               ExtraItem(lambda world: time_sensitive({(IC.progression if furfur_plush_enabled(world) else IC.filler): 1})(world)),
    "Furfur Altar Leg 2":                               ExtraItem(lambda world: buried({(IC.progression if furfur_plush_enabled(world) else IC.filler): 1})(world)),
    "Furfur Altar Top":                                 ExtraItem(lambda world: buried(time_sensitive({(IC.progression if furfur_plush_enabled(world) else IC.filler): 1}))(world)),

    # "Lead Pipe":                                        ExtraItem({IC.useful: 1}),
    "Axe":                                              ExtraItem({IC.useful: 1}),
    "Bike Helmet":                                      ExtraItem({IC.useful: 1}),
    "Digital Map":                                      ExtraItem({IC.useful: 1}),
    "Progressive Processing Speed":                     ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Download Speed":                       ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Detector Strength":                    ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Cursor Drift":                         ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Cursor Speed":                         ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Ping Cooldown":                        ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Progressive Ping Speed":                           ExtraItem(upgrade({IC.useful: 8, IC.filler: 8})),
    "Physical Module (Storm Filter)":                   ExtraItem(module({IC.useful: 1})),
    "Physical Module (Automatic Polarity Adjustment)":  ExtraItem(module({IC.useful: 1})),
    "Physical Module (Automatic Signal Processing)":    ExtraItem(module({IC.useful: 1})),
    "Physical Module (Global Alert)":                   ExtraItem(module({IC.useful: 1})),
    "Physical Module (Coordinate Triangle Visualise)":  ExtraItem(module({IC.useful: 1})),
    "Physical Module (Radar Colors)":                   ExtraItem(module({IC.useful: 1})),
    "ATV Upgrade (Big Lights)":                         ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Bumper)":                             ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Belt)":                               ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Overcharged Engine)":                 ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Alternator)":                         ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Container)":                          ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Solar Panel)":                        ExtraItem(atv_upgrade({IC.useful: 1})),
    "ATV Upgrade (Map)":                                ExtraItem(atv_upgrade({IC.useful: 1})),
    "Progressive Sleeping Bag":                         ExtraItem(recipe({IC.useful: 3})),
    "Rubber Scrap Recipe":                              ExtraItem(recipe({IC.useful: 1})),
    "Paper Scrap Recipe":                               ExtraItem(recipe({IC.useful: 1})),
    "Wood Scrap Recipe":                                ExtraItem(recipe({IC.useful: 1})),
    "Toolbox":                                          ExtraItem({IC.useful: 1, IC.filler: 3}),
    "Car Battery Charger":                              ExtraItem({IC.useful: 1}),
    "First Aid Medkit":                                 ExtraItem({IC.useful: 1}),
    "Jar of Honey":                                     ExtraItem({IC.useful: 1}),

    "Chicken Sandwich":                                 ExtraItem(plus({IC.filler: 19}, buried({IC.filler: 1}), time_sensitive({IC.filler: 1}))),
    "Rubble Recipe":                                    ExtraItem(recipe({IC.filler: 1})),
    "Air Tablet":                                       ExtraItem(buried({IC.filler: 1})),
    "Fire Tablet":                                      ExtraItem(buried({IC.filler: 1})),
    "Earth Tablet":                                     ExtraItem(buried({IC.filler: 1})),
    "Water Tablet":                                     ExtraItem(buried({IC.filler: 1})),
    "Progressive Radar History":                        ExtraItem(upgrade({IC.filler: 3})),
    "Progressive Radar Speed":                          ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Detector Frequency":                   ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Detector Quality":                     ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Coordinate Speed":                     ExtraItem(upgrade({IC.filler: 16})),
    "Progressive Breaker Time":                         ExtraItem(upgrade({IC.filler: 16})),
    "Physical Module (Radar Alarm)":                    ExtraItem({IC.filler: 1}),
    "Physical Module (Radar Radius)":                   ExtraItem({IC.filler: 1}),
    "Physical Module (Radar Path Tracking)":            ExtraItem({IC.filler: 1}),
    "Physical Module (Radar Radial Search)":            ExtraItem({IC.filler: 1}),
    "Physical Module (Autosave Signal to Database)":    ExtraItem({IC.filler: 1}),
    "Physical Module (Log Tapes Compression)":          ExtraItem({IC.filler: 1}),
    "Physical Module (Lightning Prediction)":           ExtraItem({IC.filler: 1}),
    "Physical Module (Spectrogram)":                    ExtraItem({IC.filler: 1}),
    "Physical Module (Remote Keyboard)":                ExtraItem({IC.filler: 1}),
    "ATV Upgrade (Radio)":                              ExtraItem({IC.filler: 1}),
    "ATV Upgrade (Floaties)":                           ExtraItem({IC.filler: 1}),
    "ATV Upgrade (Air Control)":                        ExtraItem({IC.filler: 1}),
    "Kerfur-Omega Documents Binder":                    ExtraItem({IC.filler: 1}),
    "Geiger Counter":                                   ExtraItem({IC.filler: 1}),
    "EMF Detector":                                     ExtraItem(buried({IC.filler: 1})),
    "Lantern":                                          ExtraItem({IC.filler: 1}),
    "Watering Can":                                     ExtraItem({IC.filler: 3}),
    "Deer Skull":                                       ExtraItem({IC.filler: 1}),
    "Antibreather Plush":                               ExtraItem(time_sensitive({IC.filler: 1})),
    "Erie Plush":                                       ExtraItem(buried(time_sensitive({IC.filler: 1}))),
    "Monique Plush":                                    ExtraItem({IC.filler: 1}),
    "Furfur Plush":                                     ExtraItem(lambda world: {IC.filler: 1} if furfur_plush_enabled(world) else {}),
    "Cacti":                                            ExtraItem(buried({IC.filler: 1})),
    "Librarian Candle":                                 ExtraItem(buried({IC.filler: 1})),
    "Car Keys":                                         ExtraItem({IC.filler: 1}),
    "Cooking Book":                                     ExtraItem({IC.filler: 1}),
    "Nuclear Pink Argemia Plush":                       ExtraItem(argemia_plush(ArgemiaPlushes.option_all, {IC.filler: 1})),
    "Nuclear Yellow Argemia Plush":                     ExtraItem(argemia_plush(ArgemiaPlushes.option_all, buried({IC.filler: 1}))),
    "Nuclear Orange Argemia Plush":                     ExtraItem(argemia_plush(ArgemiaPlushes.option_all, {IC.filler: 1})),
    "Seed Pack (The Thingy)":                           ExtraItem({IC.filler: 1}),
    "\"Svenskfisk\"":                                   ExtraItem({IC.filler: 1}),
    "Tinfoil Hat":                                      ExtraItem({IC.filler: 1}),
    "Old Rifle":                                        ExtraItem({IC.filler: 1}),
    "Ammo Box":                                         ExtraItem({IC.filler: 1}),
    "Wall Clock":                                       ExtraItem({IC.filler: 1}),
    "Unknown Fruit":                                    ExtraItem({IC.filler: 1}),
    "Bowtie":                                           ExtraItem({IC.filler: 2}),
    "Glasses":                                          ExtraItem({IC.filler: 2}),
    "Badge":                                            ExtraItem({IC.filler: 2}),
    "Jacket":                                           ExtraItem({IC.filler: 2}),
    "Compost Bucket":                                   ExtraItem({IC.filler: 2}),
    "Green Fire Rock":                                  ExtraItem(time_sensitive({IC.filler: 1})),
    "Bonus Points":                                     ExtraItem({IC.filler: 1}),

    # Previously shuffled, but I think it's better to just have the player keep them when found
    # "Maxwell":                                          ExtraItem(funny({IC.filler: 1})),
    # "Argemwell":                                        ExtraItem(funny({IC.filler: 1})),
    # "Gnarpwell":                                        ExtraItem(funny({IC.filler: 1})),
    # "Eriewell":                                         ExtraItem(funny({IC.filler: 1})),
    "Thiccfus Plush":                                   ExtraItem(funny({IC.filler: 1})),
    "Perkele Llama":                                    ExtraItem(funny({IC.filler: 1})),
    "Maid outfit":                                      ExtraItem(funny(buried({IC.filler: 1}))),

    "Ragdoll Trap":                                     ExtraItem({IC.trap: 1}),
    "Breaker Trap":                                     ExtraItem({IC.trap: 1}),
    "Debug TP Trap":                                    ExtraItem({IC.trap: 1}),
    "Drunk Trap":                                       ExtraItem({IC.trap: 1}),
    "Points Fine Trap":                                 ExtraItem({IC.trap: 1}),
    "Flat Tire Trap":                                   ExtraItem({IC.trap: 1}),
    "Dead Flashlight Trap":                             ExtraItem({IC.trap: 1})
}
