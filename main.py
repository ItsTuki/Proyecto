from flask import Flask, request, jsonify, send_from_directory
import discord
from discord.ext import commands
from threading import Thread

app = Flask(__name__)

# Lista de posts
posts = []

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    index = data.get('index')
    vote_type = data.get('type')

    if 0 <= index < len(posts):
        if vote_type == 'up':
            posts[index]['votes'] += 1
        elif vote_type == 'down':
            posts[index]['votes'] -= 1
        return jsonify(posts)
    else:
        return {'error': 'Post no encontrado'}, 404

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Configuración del bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot está listo como {bot.user}')

@bot.command(name='addpost')
async def add_post(ctx, title: str, *, description: str):
    new_post = {'title': title, 'description': description, 'votes': 0}
    posts.append(new_post)

    # Enviar el mensaje y agregar reacciones
    message = await ctx.send(f'Post agregado: **{title}**\n{description}')
    await message.add_reaction('⬆️')  # Upvote
    await message.add_reaction('⬇️')  # Downvote

@bot.command(name='loadposts')
async def load_posts_command(ctx):
    global posts
    posts = []  # Reiniciar la lista de posts

    async for message in ctx.channel.history(limit=100):  # Limitar a los últimos 100 mensajes
        if message.content.startswith('Post agregado: **'):
            title_start = message.content.find('**') + 2
            title_end = message.content.find('**', title_start)
            title = message.content[title_start:title_end]

            description = message.content.split('\n')[1]  # Suponiendo que la descripción está en la segunda línea

            # Crear un nuevo post
            new_post = {'title': title, 'description': description, 'votes': 0}
            posts.append(new_post)

    await ctx.send('Posts cargados desde el canal.')

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return  # Ignorar reacciones del bot

    if reaction.emoji == '⬆️':
        for post in posts:
            if reaction.message.content.startswith(f'Post agregado: **{post["title"]}**'):
                post['votes'] += 1
                await reaction.message.channel.send(f'¡Voto a favor de {post["title"]}! Votos: {post["votes"]}')
                break

    elif reaction.emoji == '⬇️':
        for post in posts:
            if reaction.message.content.startswith(f'Post agregado: **{post["title"]}**'):
                post['votes'] -= 1
                await reaction.message.channel.send(f'¡Voto en contra de {post["title"]}! Votos: {post["votes"]}')
                break

if __name__ == '__main__':
    # Ejecutar Flask en un hilo separado
    Thread(target=run_flask).start()
    # Iniciar el bot de Discord
    bot.run('MTIyNTIzMTc5MDE5NzcwNjkxNQ.GZrJTM.Bh86Yr7N8oFphDbSQozbyNWKicMjcAfHR-n_Hs') 
