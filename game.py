import discord
from discord.ext import commands
import random
import json

# Khởi tạo bot
bot = commands.Bot(command_prefix='!')

# Load dữ liệu người chơi từ tệp players.json
def load_player_data():
    try:
        with open('players.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Lưu dữ liệu người chơi vào tệp players.json
def save_player_data(data):
    with open('players.json', 'w') as file:
        json.dump(data, file)

# Load dữ liệu vật phẩm từ tệp items.json
def load_items_data():
    try:
        with open('items.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Lệnh hunt với cải tiến
@bot.command()
async def hunt(ctx):
    user_id = str(ctx.author.id)

    player_data = load_player_data()
    animals_data = load_animals_data()

    if user_id not in player_data:
        player_data[user_id] = {'points': 0, 'money': 0, 'items': []}

    hunted_animal = random.choices(list(animals_data.keys()), weights=[animal['chance'] for animal in animals_data.values()])[0]
    animal = animals_data[hunted_animal]

    if random.random() <= animal['chance']:
        player_data[user_id]['points'] += animal['points']
        player_data[user_id]['money'] += animal['money']
        await ctx.send(f"Bạn đã săn được một con {hunted_animal}. 🎯 +{animal['points']} điểm và +{animal['money']} tiền")
    else:
        player_data[user_id]['points'] -= 1
        await ctx.send(f"Rất tiếc! Bạn đã không săn được con {hunted_animal}. 🙁 -1 điểm")

    save_player_data(player_data)

# Lệnh để xem thông tin người chơi
@bot.command()
async def profile(ctx):
    user_id = str(ctx.author.id)

    player_data = load_player_data()

    if user_id not in player_data:
        await ctx.send("Bạn chưa có hồ sơ người chơi.")
    else:
        points = player_data[user_id]['points']
        money = player_data[user_id]['money']
        items = ', '.join(player_data[user_id]['items'])
        await ctx.send(f"Thông tin người chơi:\nĐiểm: {points}\nTiền: {money}\nVật phẩm: {items}")

# Lệnh để xem cửa hàng và mua vật phẩm
@bot.command()
async def shop(ctx):
    items_data = load_items_data()
    items = list(items_data.keys())
    item = random.choice(items)
    price = items_data[item]['price']

    await ctx.send(f"Cửa hàng có {item} với giá {price} tiền. Sử dụng lệnh !buy {item.lower()} để mua.")

# Lệnh để mua vật phẩm
@bot.command()
async def buy(ctx, item_name):
    user_id = str(ctx.author.id)

    player_data = load_player_data()
    items_data = load_items_data()

    if user_id not in player_data:
        player_data[user_id] = {'points': 0, 'money': 0, 'items': []}

    if item_name not in items_data:
        await ctx.send(f"Vật phẩm '{item_name}' không tồn tại trong cửa hàng.")
    else:
        price = items_data[item_name]['price']
        if player_data[user_id]['money'] >= price:
            player_data[user_id]['money'] -= price
            player_data[user_id]['items'].append(item_name)
            await ctx.send(f"Bạn đã mua thành công vật phẩm '{item_name}' với giá {price} tiền.")
        else:
            await ctx.send("Bạn không có đủ tiền để mua vật phẩm này.")

    save_player_data(player_data)

# Khởi động bot
bot.run('YOUR_BOT_TOKEN')
