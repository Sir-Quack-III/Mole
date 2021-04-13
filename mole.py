import discord
from discord.ext import commands
from PyDictionary import PyDictionary
import time
import wikipedia_for_humans
import requests
from bs4 import BeautifulSoup

dictionary = PyDictionary()

client = commands.Bot(command_prefix = "~")

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")

@commands.command()
async def dict(ctx, arg, word):
    if arg == "define":
        try:
            full_definition = dictionary.meaning(str(word))
            ctx.send(f"**Results for {word}:**")
            for x in full_definition:
                for ele in full_definition[x]:
                    await ctx.send(f"**{x}:** {ele}")
            time.sleep(0.5)
        except:
            await ctx.send(f"**ERROR:** Your word, '*{word}*' was not found in our library!")

    if arg == "synonym":
        try:
            synonym = dictionary.synonym(str(word))
            await ctx.send(f"**Results for {word}:**")
            await ctx.send(", ".join(synonym))
        except:
            await ctx.send(f"**ERROR:** Your word, '*{word}*' was not found in our library!")

    if arg == "antonym":
        try:
            antonym = dictionary.antonym(str(word))
            await ctx.send(f"**Results for {word}:**")
            await ctx.send(", ".join(antonym))
        except:
            await ctx.send(f"**ERROR:** Your word, '*{word}*' was not found in our library!")

@commands.command()
async def wiki(ctx, arg, word):

    if arg == "summary":
        summary = wikipedia_for_humans.summary(str(word)).split(". ")

        r = requests.get(wikipedia_for_humans.page_data(word)["url"])
        soup = BeautifulSoup(r.text, "lxml")
        img = soup.find("div", {"class":"thumbinner"})

        await ctx.send(f"**Top Result for '{word}'**")
        await ctx.send(f"https:{img.a.img['src']}")

        for ele in summary:
            await ctx.send(ele)

    if arg == "gallery":
        r = requests.get(wikipedia_for_humans.page_data(word)["url"])
        soup = BeautifulSoup(r.text, "lxml")
        imgs = soup.findAll("div", {"class":"thumbinner"})
        for img in imgs:
            try:
                await ctx.send(f"https:{img.a.img['src']}")
                await ctx.send(f"{img.a.text} \n\n")
            except:
                pass
            time.sleep(0.5)

@commands.command()
async def web(ctx, arg, site):
    if arg == "sum":
        r = requests.get(f"https://{site}")
        soup = BeautifulSoup(r.text, "lxml")
        h = soup.h1.text
        p = soup.p.text
        
        await ctx.send(f"**{h}**")
        await ctx.send(p)
    if arg == "gallery":
        r = requests.get(f"https://{site}")
        soup = BeautifulSoup(r.text, "lxml")
        imgs = soup.findAll("img")
        for x in imgs:
            await ctx.send(f"https://{x['src']}")

client.add_command(web)
client.add_command(dict)
client.add_command(wiki)

client.run("insert token here")
