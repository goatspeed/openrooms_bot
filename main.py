import os
from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto,
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler, filters,
)
from supabase import create_client

# --- Credentials & Setup ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ROOM_TYPES = ['Single', 'Double', 'Triple', 'Four']

# --- States: Each field is its own state; no overlap! ----
(
    MAIN_MENU,
    TENANT_ROOM_TYPE,
    TENANT_LISTING_NAV,
    OWNER_ONBOARD_PG,
    OWNER_ONBOARD_NAME,
    OWNER_ONBOARD_PHONE,
    OWNER_ONBOARD_ADDRESS,
    OWNER_ONBOARD_FEATURES,
    OWNER_ONBOARD_PRICING,
    OWNER_ONBOARD_MAPLINK,
    OWNER_ROOM_TYPE,
    OWNER_ROOM_PHOTOS,
    OWNER_CONFIRM,
    OWNER_UPDATE_MENU,
    OWNER_UPDATE_CHOICE,
    OWNER_UPDATE_PHONE,
    OWNER_UPDATE_ROOM_AVAIL,
    OWNER_UPDATE_ADD_PHOTOS,
    OWNER_UPDATE_ORDER_PHOTOS,
) = range(19)

TENANT, OWNER = "tenant", "owner"

# --- Utility: Format features for bullet-point display ---
def format_features_bullets(features_text):
    if not features_text:
        return "N/A"
    features = [f.strip() for f in features_text.split(",") if f.strip()]
    return "\n" + "\n".join(f"• {f}" for f in features)

# --- Helper for Owner Onboarding Navigation ---
OWNER_FIELDS = [
    ('pg_name', 'Please enter your PG name:'),
    ('owner_name', 'Your full name:'),
    ('phone_number', 'Your phone number:'),
    ('address', 'PG address:'),
    ('features', 'List some features (comma-separated):'),
    ('pricing', 'Approximate pricing (e.g., ₹5000-₹7000):'),
    ('map_link', 'Google Maps link to your PG:'),
]

# --- Helper: Which state comes after which field? ---
def get_next_owner_field_state(current_field):
    field_order = [
        ('pg_name', OWNER_ONBOARD_PG, OWNER_ONBOARD_NAME),
        ('owner_name', OWNER_ONBOARD_NAME, OWNER_ONBOARD_PHONE),
        ('phone_number', OWNER_ONBOARD_PHONE, OWNER_ONBOARD_ADDRESS),
        ('address', OWNER_ONBOARD_ADDRESS, OWNER_ONBOARD_FEATURES),
        ('features', OWNER_ONBOARD_FEATURES, OWNER_ONBOARD_PRICING),
        ('pricing', OWNER_ONBOARD_PRICING, OWNER_ONBOARD_MAPLINK),
        ('map_link', OWNER_ONBOARD_MAPLINK, OWNER_ROOM_TYPE),
    ]
    for field, cur_state, next_state in field_order:
        if current_field == field:
            return next_state
    return OWNER_ROOM_TYPE  # fallback

# --- Helper: Send "UPDATE" / "CONFIRM" buttons for any onboarding field ---
async def send_update_confirm(update, field_label, val):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("UPDATE", callback_data="update_field")],
        [InlineKeyboardButton("CONFIRM", callback_data="confirm_field")]
    ])
    await update.message.reply_text(
        f"{field_label}: {val}\n\nChoose an option below or type again to update.",
        reply_markup=kb
    )

# --- End of Part 1 ---

# ✔️ When ready, say "part 2" and you’ll get all your handlers, main flows, and no duplication!

import os
from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,
    KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto,
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, 
    ContextTypes, ConversationHandler, filters,
)
from supabase import create_client

# --- Credentials & Setup ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

ROOM_TYPES = ['Single', 'Double', 'Triple', 'Four']

# --- States ---
(
    MAIN_MENU,
    TENANT_ROOM_TYPE,
    TENANT_LISTING_NAV,
    OWNER_ONBOARD_PG,
    OWNER_ONBOARD_NAME,
    OWNER_ONBOARD_PHONE,
    OWNER_ONBOARD_ADDRESS,
    OWNER_ONBOARD_FEATURES,
    OWNER_ONBOARD_PRICING,
    OWNER_ONBOARD_MAPLINK,
    OWNER_ROOM_TYPE,
    OWNER_ROOM_PHOTOS,
    OWNER_CONFIRM,
    OWNER_UPDATE_MENU,
    OWNER_UPDATE_CHOICE,
    OWNER_UPDATE_PHONE,
    OWNER_UPDATE_ROOM_AVAIL,
    OWNER_UPDATE_ADD_PHOTOS,
    OWNER_UPDATE_ORDER_PHOTOS,
) = range(19)

TENANT, OWNER = "tenant", "owner"

# --- Utilities ---

def format_features_bullets(features_text):
    if not features_text:
        return "N/A"
    features = [f.strip() for f in features_text.split(",") if f.strip()]
    return "\n" + "\n".join(f"• {f}" for f in features)

# Helper for Owner Onboarding state navigation
def get_next_owner_field_state(current_field):
    field_order = [
        ('pg_name', OWNER_ONBOARD_PG, OWNER_ONBOARD_NAME),
        ('owner_name', OWNER_ONBOARD_NAME, OWNER_ONBOARD_PHONE),
        ('phone_number', OWNER_ONBOARD_PHONE, OWNER_ONBOARD_ADDRESS),
        ('address', OWNER_ONBOARD_ADDRESS, OWNER_ONBOARD_FEATURES),
        ('features', OWNER_ONBOARD_FEATURES, OWNER_ONBOARD_PRICING),
        ('pricing', OWNER_ONBOARD_PRICING, OWNER_ONBOARD_MAPLINK),
        ('map_link', OWNER_ONBOARD_MAPLINK, OWNER_ROOM_TYPE),
    ]
    for field, cur_state, next_state in field_order:
        if current_field == field:
            return next_state
    return OWNER_ROOM_TYPE

async def send_update_confirm(update, field_label, val):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("UPDATE", callback_data="update_field")],
        [InlineKeyboardButton("CONFIRM", callback_data="confirm_field")]
    ])
    await update.message.reply_text(
        f"{field_label}: {val}\n\nChoose an option below, or type again to update.",
        reply_markup=kb
    )

# ----- End of PART 1 -----
# Next: Part 2 will include start/menu handlers, the full tenant flow, and the per-field owner onboarding steps.

# --- START & MAIN MENU HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔍 Searching for PG", "🏢 I'm a PG Owner"],
        ["/restart"],
    ]
    await update.message.reply_text(
        "Welcome to Open Rooms! Please choose:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return MAIN_MENU

async def main_menu(update, context):
    await start(update, context)
    return MAIN_MENU

async def restart(update, context):
    await start(update, context)
    return MAIN_MENU

# --- TENANT FLOW ---

async def tenant_start(update, context):
    keyboard = [
        ROOM_TYPES[:2],
        ROOM_TYPES[2:] + ["Back"],
        ["Main Menu", "/restart"]
    ]
    await update.message.reply_text(
        "Choose your preferred room type:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return TENANT_ROOM_TYPE

async def tenant_select_room_type(update, context):
    room_type = update.message.text.strip().lower()
    if room_type not in [r.lower() for r in ROOM_TYPES]:
        await update.message.reply_text("Invalid choice. Try again.")
        return TENANT_ROOM_TYPE
    context.user_data['room_type'] = room_type

    room_query = (
        supabase.from_("rooms")
        .select("*,pg_id")
        .eq("room_type", room_type)
        .eq("is_available", True)
    ).execute()
    rooms = room_query.data or []
    if not rooms:
        await update.message.reply_text(
            "No PGs found for this room type. Try another.",
            reply_markup=ReplyKeyboardMarkup([["Back", "Main Menu", "/restart"]], resize_keyboard=True)
        )
        return TENANT_ROOM_TYPE

    pg_ids = list(set([r['pg_id'] for r in rooms]))
    pg_query = supabase.from_("pg_listings").select("*").in_("id", pg_ids).execute()
    pgs = {pg['id']: pg for pg in (pg_query.data or [])}

    context.user_data['search_list'] = [
        {"pg": pgs[room['pg_id']], "room": room}
        for room in rooms if room['pg_id'] in pgs
    ]
    context.user_data['search_idx'] = 0
    return await show_pg_to_tenant(update, context)

async def show_pg_to_tenant(update, context):
    idx = context.user_data.get('search_idx', 0)
    listings = context.user_data.get('search_list', [])
    if not listings:
        await update.message.reply_text(
            "No listings to show.",
            reply_markup=ReplyKeyboardMarkup([["Back", "Main Menu"]], resize_keyboard=True)
        )
        return TENANT_ROOM_TYPE
    listing = listings[idx]
    pg = listing["pg"]
    room = listing["room"]
    img_query = supabase.from_("room_images").select("*").eq("room_id", room["id"]).order("ordering").limit(1).execute()
    photo_id = img_query.data[0]['telegram_file_id'] if img_query.data else None
    owner_data = supabase.from_("users").select("*").eq("id", pg["owner_id"]).single().execute().data
    phone = owner_data["phone_number"] if owner_data else "Not available"
    features_md = format_features_bullets(pg.get('features', ''))
    msg = (
        f"🏠 {pg['pg_name']}\n"
        f"📍 {pg['address']}\n"
        f"🛏️ Features:{features_md}\n"
        f"💰 Price: {pg.get('pricing','N/A')} | Rent: ₹{room.get('price','N/A')}, Food: ₹{room.get('food_price','N/A')}\n"
        f"📞 Phone: {phone}\n"
        f"🗺️ [View on Map]({pg.get('map_link','')})\n"
        f"Availability: {'✅' if room['is_available'] else '❌'}"
    )
    buttons = [
        [
            InlineKeyboardButton("Contact PG Owner", callback_data=f"tenant_contact_{phone}"),
            InlineKeyboardButton("Next PG", callback_data="tenant_next_pg")
        ],
        [
            InlineKeyboardButton("Back", callback_data="tenant_back"),
            InlineKeyboardButton("Main Menu", callback_data="main_menu"),
            InlineKeyboardButton("Restart", callback_data="restart"),
        ],
    ]
    if photo_id:
        await update.message.reply_photo(
            photo=photo_id, caption=msg, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await update.message.reply_text(
            msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons),
        )
    return TENANT_LISTING_NAV

async def tenant_inline_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    idx = context.user_data.get('search_idx', 0)
    listings = context.user_data.get('search_list', [])
    if data == "tenant_next_pg":
        idx = idx + 1 if idx + 1 < len(listings) else 0
        context.user_data['search_idx'] = idx
        await query.delete_message()
        return await show_pg_to_tenant(query, context)
    elif data.startswith("tenant_contact_"):
        phone = data[len("tenant_contact_") :]
        await query.message.reply_text(f"📞 Contact Owner: {phone}")
        return TENANT_LISTING_NAV
    elif data == "tenant_back":
        await main_menu(update, context)
        return MAIN_MENU
    elif data == "main_menu":
        await main_menu(update, context)
        return MAIN_MENU
    elif data == "restart":
        await start(update, context)
        return MAIN_MENU
    return TENANT_LISTING_NAV

# --- OWNER FIELD-BY-FIELD ONBOARDING ---

# PG Name
async def owner_start(update, context):
    context.user_data['owner_data'] = {}
    await update.message.reply_text("Please enter your PG name:")
    return OWNER_ONBOARD_PG

async def owner_pg_name(update, context):
    context.user_data['owner_data']['pg_name'] = update.message.text
    await send_update_confirm(update, "PG Name", update.message.text)
    context.user_data['pending_field'] = 'pg_name'
    return OWNER_ONBOARD_NAME

async def owner_name(update, context):
    context.user_data['owner_data']['owner_name'] = update.message.text
    await send_update_confirm(update, "Owner Name", update.message.text)
    context.user_data['pending_field'] = 'owner_name'
    return OWNER_ONBOARD_PHONE

async def owner_phone(update, context):
    context.user_data['owner_data']['phone_number'] = update.message.text
    await send_update_confirm(update, "Phone Number", update.message.text)
    context.user_data['pending_field'] = 'phone_number'
    return OWNER_ONBOARD_ADDRESS

async def owner_address(update, context):
    context.user_data['owner_data']['address'] = update.message.text
    await send_update_confirm(update, "Address", update.message.text)
    context.user_data['pending_field'] = 'address'
    return OWNER_ONBOARD_FEATURES

async def owner_features(update, context):
    context.user_data['owner_data']['features'] = update.message.text
    await send_update_confirm(update, "Features", update.message.text)
    context.user_data['pending_field'] = 'features'
    return OWNER_ONBOARD_PRICING

async def owner_pricing(update, context):
    context.user_data['owner_data']['pricing'] = update.message.text
    await send_update_confirm(update, "Pricing", update.message.text)
    context.user_data['pending_field'] = 'pricing'
    return OWNER_ONBOARD_MAPLINK

async def owner_map_link(update, context):
    context.user_data['owner_data']['map_link'] = update.message.text
    await send_update_confirm(update, "Google Maps Link", update.message.text)
    context.user_data['pending_field'] = 'map_link'
    return OWNER_ONBOARD_MAPLINK


# --- End of Part 3 ---

# Next: Part 4 gives the handlers for processing the "UPDATE"/"CONFIRM" buttons, room/photo upload, and confirmation flows.

# --- OWNER ONBOARDING: Handle UPDATE/CONFIRM Buttons and Field Transitions ---

async def owner_update_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    field = context.user_data.get('pending_field', None)
    owner_data = context.user_data.get('owner_data', {})
    # Mapping for prompts and state progress
    field_prompts = {
        'pg_name': 'Please enter your PG name:',
        'owner_name': 'Your full name:',
        'phone_number': 'Your phone number:',
        'address': 'PG address:',
        'features': 'List some features (comma-separated):',
        'pricing': 'Approximate pricing (e.g., ₹5000-₹7000):',
        'map_link': 'Google Maps link to your PG:'
    }
    state_map = {
        'pg_name': OWNER_ONBOARD_PG,
        'owner_name': OWNER_ONBOARD_NAME,
        'phone_number': OWNER_ONBOARD_PHONE,
        'address': OWNER_ONBOARD_ADDRESS,
        'features': OWNER_ONBOARD_FEATURES,
        'pricing': OWNER_ONBOARD_PRICING,
        'map_link': OWNER_ONBOARD_MAPLINK,
    }
    if data == "update_field" and field:
        await query.message.reply_text(field_prompts[field])
        return state_map[field]
    elif data == "confirm_field" and field:
        next_state = get_next_owner_field_state(field)
        next_field_prompts = {
            OWNER_ONBOARD_NAME: "Your full name:",
            OWNER_ONBOARD_PHONE: "Your phone number:",
            OWNER_ONBOARD_ADDRESS: "PG address:",
            OWNER_ONBOARD_FEATURES: "List some features (comma-separated):",
            OWNER_ONBOARD_PRICING: "Approximate pricing (e.g., ₹5000-₹7000):",
            OWNER_ONBOARD_MAPLINK: "Google Maps link to your PG:"
        }
        if next_state != OWNER_ROOM_TYPE:
            # only show the next prompt if not entering room step
            if next_state in next_field_prompts:
                await query.message.reply_text(next_field_prompts[next_state])
            return next_state
        else:
            keyboard = [ROOM_TYPES[:2], ROOM_TYPES[2:] + ["Done Adding Rooms"]]
            await query.message.reply_text(
                "Select room type to add photos:",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
            context.user_data.setdefault('owner_rooms', [])
            return OWNER_ROOM_TYPE
    # fallback
    if field:
        await query.message.reply_text(field_prompts.get(field, "Please try again:"))
        return state_map.get(field, OWNER_ONBOARD_PG)
    else:
        await query.message.reply_text("Please start again (/start).")
        return OWNER_ONBOARD_PG

# --- ROOM PHOTO UPLOAD AND CONFIRMATION FLOW ---

async def owner_room_type(update, context):
    room_type = update.message.text
    if room_type.lower() == "done adding rooms":
        # Show summary for confirmation
        owner = context.user_data['owner_data']
        summary = (
            f"PG Name: {owner.get('pg_name')}\nFull Name: {owner.get('owner_name')}\n"
            f"Phone: {owner.get('phone_number')}\nAddress: {owner.get('address')}\n"
            f"Features: {owner.get('features')}\nPricing: {owner.get('pricing')}\n"
            f"Map Link: {owner.get('map_link')}\nRooms: {len(context.user_data['owner_rooms'])}"
        )
        await update.message.reply_text(
            f"Please confirm your listing:\n\n{summary}",
            reply_markup=ReplyKeyboardMarkup([["Confirm & Submit", "Edit Any Info", "Main Menu", "/restart"]], resize_keyboard=True)
        )
        return OWNER_CONFIRM
    elif room_type not in ROOM_TYPES:
        await update.message.reply_text("Invalid room type. Please choose from the buttons.")
        return OWNER_ROOM_TYPE
    else:
        context.user_data['current_room_type'] = room_type
        context.user_data['photos'] = []
        await update.message.reply_text(
            f"Now upload photos for {room_type} room (send all, then /done when finished):",
            reply_markup=ReplyKeyboardMarkup([["/done"]], resize_keyboard=True)
        )
        return OWNER_ROOM_PHOTOS

async def owner_room_photo(update, context):
    # Accept each photo
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        context.user_data['photos'].append(file_id)
        await update.message.reply_text("Photo received! Send more, or /done.")
    return OWNER_ROOM_PHOTOS

async def owner_room_photos_done(update, context):
    # Save this room type with all uploaded photo file_ids
    context.user_data['owner_rooms'].append({
        "room_type": context.user_data['current_room_type'],
        "photos": context.user_data['photos']
    })
    keyboard = [ROOM_TYPES[:2], ROOM_TYPES[2:] + ["Done Adding Rooms"]]
    await update.message.reply_text(
        "Added! Want to add another room type? Or tap 'Done Adding Rooms'.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return OWNER_ROOM_TYPE

# --- FINAL CONFIRM/SUBMIT (save to Supabase) ---

async def owner_confirm(update, context):
    text = update.message.text.strip().lower()
    if "confirm" in text:
        owner = context.user_data.get('owner_data', {})
        rooms_info = context.user_data.get('owner_rooms', [])
        # Insert or upsert owner
        users_resp = supabase.from_("users").select("id").eq("telegram_id", update.effective_user.id).execute()
        if users_resp.data:
            user_id = users_resp.data[0]["id"]
            supabase.from_("users").update({"phone_number": owner["phone_number"]}).eq("id", user_id).execute()
        else:
            user_ins = supabase.from_("users").insert({
                "telegram_id": update.effective_user.id,
                "user_type": "owner",
                "full_name": owner.get("owner_name"),
                "phone_number": owner.get("phone_number")
            }).execute()
            user_id = user_ins.data[0]["id"]
        # Insert PG
        pg_ins = supabase.from_("pg_listings").insert({
            "owner_id": user_id,
            "pg_name": owner['pg_name'],
            "address": owner['address'],
            "features": owner['features'],
            "pricing": owner['pricing'],
            "map_link": owner['map_link']
        }).execute()
        pg_id = pg_ins.data[0]["id"]
        # Insert rooms & images
        for room in rooms_info:
            room_type = room["room_type"].lower()
            room_add = supabase.from_("rooms").insert({
                "pg_id": pg_id, "room_type": room_type,
                "price": None,
                "food_price": None,
                "is_available": True,
                "order_no": 1,
            }).execute()
            room_id = room_add.data[0]["id"]
            for order_idx, file_id in enumerate(room['photos'], start=1):
                supabase.from_("room_images").insert({
                    "room_id": room_id,
                    "ordering": order_idx,
                    "telegram_file_id": file_id,
                    "image_url": None
                }).execute()
        await update.message.reply_text(
            "PG listing submitted successfully!\n\nUse /update to edit or add more in future.",
            reply_markup=ReplyKeyboardMarkup([["Main Menu", "/restart"]], resize_keyboard=True)
        )
        context.user_data.clear()
        return MAIN_MENU
    elif "edit" in text:
        await update.message.reply_text("Please restart /start to edit info.", reply_markup=ReplyKeyboardMarkup([["/restart"]], resize_keyboard=True))
        context.user_data.clear()
        return MAIN_MENU
    elif "main menu" in text:
        await main_menu(update, context)
        context.user_data.clear()
        return MAIN_MENU
    else:
        await update.message.reply_text("Please choose 'Confirm & Submit' or edit information.")
        return OWNER_CONFIRM

# -------- END OF PART 4 ----------
# Part 5 will give: the owner update/edit menu, handlers for live-edit (phone, availability, photos), and utility handler functions.

# --- OWNER UPDATE/EDIT MENU & UPDATE HANDLERS ---

async def owner_update(update, context):
    users_resp = supabase.from_("users").select("id").eq("telegram_id", update.effective_user.id).execute()
    if not users_resp.data:
        await update.message.reply_text("No profile found. Please use /start to create an owner profile.")
        return MAIN_MENU
    user_id = users_resp.data[0]["id"]
    pg_resp = supabase.from_("pg_listings").select("*").eq("owner_id", user_id).execute()
    pgs = pg_resp.data or []
    if not pgs:
        await update.message.reply_text("You have no PGs yet.")
        return MAIN_MENU
    buttons = [[InlineKeyboardButton(pg["pg_name"], callback_data=f"update_pg_{pg['id']}")] for pg in pgs]
    await update.message.reply_text("Choose PG to update:", reply_markup=InlineKeyboardMarkup(buttons))
    context.user_data['owner_pgs'] = {pg['id']: pg for pg in pgs}
    return OWNER_UPDATE_MENU

async def owner_update_menu_handler(update, context):
    query = update.callback_query
    if query.data.startswith("update_pg_"):
        pg_id = query.data.split("_")[-1]
        context.user_data['update_pg_id'] = pg_id
        buttons = [
            [InlineKeyboardButton("Edit Phone", callback_data="update_phone")],
            [InlineKeyboardButton("Edit Room Availability", callback_data="update_room_avail")],
            [InlineKeyboardButton("Add Room Photos", callback_data="update_add_photos")],
            [InlineKeyboardButton("Back", callback_data="main_menu")],
        ]
        await query.message.reply_text("What do you want to update?", reply_markup=InlineKeyboardMarkup(buttons))
        return OWNER_UPDATE_CHOICE
    return OWNER_UPDATE_MENU

async def owner_update_choice_handler(update, context):
    query = update.callback_query
    choice = query.data
    if choice == "update_phone":
        await query.message.reply_text("Enter your new phone number:")
        return OWNER_UPDATE_PHONE
    elif choice == "update_room_avail":
        pg_id = context.user_data['update_pg_id']
        rooms = supabase.from_("rooms").select("*").eq("pg_id", pg_id).execute().data or []
        btns = [
            [InlineKeyboardButton(f"{r['room_type'].capitalize()} ({'✅' if r['is_available'] else '❌'})", callback_data=f"toggle_room_{r['id']}")]
            for r in rooms
        ]
        await query.message.reply_text("Tap to Toggle Room Availability:", reply_markup=InlineKeyboardMarkup(btns))
        return OWNER_UPDATE_ROOM_AVAIL
    elif choice == "update_add_photos":
        await query.message.reply_text("Type the room type (Single/Double/Triple/Four) to add photos to it:")
        return OWNER_UPDATE_ADD_PHOTOS
    elif choice == "main_menu":
        await main_menu(update, context)
        return MAIN_MENU
    return OWNER_UPDATE_CHOICE

async def owner_update_phone_handler(update, context):
    new_number = update.message.text.strip()
    users_resp = supabase.from_("users").select("id").eq("telegram_id", update.effective_user.id).execute()
    if users_resp.data:
        user_id = users_resp.data[0]["id"]
        supabase.from_("users").update({"phone_number": new_number}).eq("id", user_id).execute()
        await update.message.reply_text(f"Phone number updated to: {new_number}")
    return MAIN_MENU

async def owner_update_room_avail_handler(update, context):
    query = update.callback_query
    if query.data.startswith("toggle_room_"):
        room_id = query.data.split("_")[-1]
        room = supabase.from_("rooms").select("*").eq("id", room_id).single().execute().data
        new_avail = not room["is_available"]
        supabase.from_("rooms").update({"is_available": new_avail}).eq("id", room_id).execute()
        await query.message.reply_text(f"{room['room_type'].capitalize()} room is now {'✅ available' if new_avail else '❌ not available'}.")
    return MAIN_MENU

async def owner_update_add_photos_handler(update, context):
    rm_type = update.message.text.strip().capitalize()
    if rm_type not in ROOM_TYPES:
        await update.message.reply_text("Invalid room type. Try again.")
        return OWNER_UPDATE_ADD_PHOTOS
    pg_id = context.user_data['update_pg_id']
    room_q = supabase.from_("rooms").select("id").eq("pg_id", pg_id).eq("room_type", rm_type.lower()).single().execute()
    if not room_q.data:
        await update.message.reply_text("Room type not found for this PG.")
        return MAIN_MENU
    context.user_data['update_room_id'] = room_q.data['id']
    context.user_data['add_photo_list'] = []
    await update.message.reply_text(f"Send images for {rm_type} room (Send all, then /done):",
                                   reply_markup=ReplyKeyboardMarkup([["/done"]], resize_keyboard=True))
    return OWNER_UPDATE_ADD_PHOTOS

async def owner_update_add_photos_collect(update, context):
    if update.message.photo:
        fid = update.message.photo[-1].file_id
        context.user_data['add_photo_list'].append(fid)
        await update.message.reply_text("Photo received! Send more or /done.")
    return OWNER_UPDATE_ADD_PHOTOS

async def owner_update_add_photos_done(update, context):
    photos = context.user_data.get('add_photo_list', [])
    room_id = context.user_data['update_room_id']
    imgs = supabase.from_("room_images").select("ordering").eq("room_id", room_id).order("ordering", desc=True).execute().data or []
    max_ord = imgs[0]['ordering'] if imgs else 0
    for idx, fid in enumerate(photos, 1):
        supabase.from_("room_images").insert({
            "room_id": room_id,
            "ordering": max_ord + idx,
            "telegram_file_id": fid,
            "image_url": None
        }).execute()
    await update.message.reply_text("Photos added!")
    return MAIN_MENU

# --- End of Part 5 ---
# Part 6: ConversationHandler wiring, dispatcher, and the main entrypoint.

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Owner onboarding and update ConversationHandler
    owner_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r"🏢 I'm a PG Owner"), owner_start)],
        states={
            # Owner onboarding, each field is a unique step—
            OWNER_ONBOARD_PG: [MessageHandler(filters.TEXT & ~filters.COMMAND, owner_pg_name)],
            OWNER_ONBOARD_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_name),
                CallbackQueryHandler(owner_update_confirm_handler),
            ],
            OWNER_ONBOARD_PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_phone),
                CallbackQueryHandler(owner_update_confirm_handler),
            ],
            OWNER_ONBOARD_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_address),
                CallbackQueryHandler(owner_update_confirm_handler),
            ],
            OWNER_ONBOARD_FEATURES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_features),
                CallbackQueryHandler(owner_update_confirm_handler),
            ],
            OWNER_ONBOARD_PRICING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_pricing),
                CallbackQueryHandler(owner_update_confirm_handler),
            ],
            OWNER_ONBOARD_MAPLINK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_map_link),
                CallbackQueryHandler(owner_update_confirm_handler),
            ],
            OWNER_ROOM_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, owner_room_type)],
            OWNER_ROOM_PHOTOS: [
                MessageHandler(filters.PHOTO, owner_room_photo),
                MessageHandler(filters.Regex(r"/done"), owner_room_photos_done),
            ],
            OWNER_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, owner_confirm)],
            # Owner update/edit menu & functionality
            OWNER_UPDATE_MENU: [CallbackQueryHandler(owner_update_menu_handler)],
            OWNER_UPDATE_CHOICE: [CallbackQueryHandler(owner_update_choice_handler)],
            OWNER_UPDATE_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, owner_update_phone_handler)],
            OWNER_UPDATE_ROOM_AVAIL: [CallbackQueryHandler(owner_update_room_avail_handler)],
            OWNER_UPDATE_ADD_PHOTOS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, owner_update_add_photos_handler),
                MessageHandler(filters.PHOTO, owner_update_add_photos_collect),
                MessageHandler(filters.Regex(r"/done"), owner_update_add_photos_done)
            ],
        },
        fallbacks=[CommandHandler("restart", restart)],
        allow_reentry=True,
    )

    # Tenant search flow ConversationHandler
    tenant_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(r"🔍 Searching for PG"), tenant_start)],
        states={
            TENANT_ROOM_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, tenant_select_room_type)],
            TENANT_LISTING_NAV: [CallbackQueryHandler(tenant_inline_handler)],
        },
        fallbacks=[CommandHandler("restart", restart)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("main_menu", main_menu))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("update", owner_update))
    app.add_handler(owner_conv)
    app.add_handler(tenant_conv)

    app.run_polling()

if __name__ == "__main__":
    main()
