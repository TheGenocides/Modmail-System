import discord
import random
import asyncio
import json
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="YOUR PREFIX HERE!", intents=intents)

with open("status.json", "r") as f:
	mod=json.load(f)

with open("modmail.json", "r") as f:
	modmail=json.load(f)
	
		
@client.event
async def on_message(msg):
	if msg.author.bot:
		return

	_id_=random.randint(1000000,9999999)
	ctx=await client.get_context(msg)
	cate=client.get_channel(CATEGORY ID HERE)
	guild=client.get_guild(YOUR SERVER ID HERE)
	role=guild.get_role(THE ROLE THAT HANDLE MODMAIL)
	
	Modmail = {
    	guild.default_role: discord.PermissionOverwrite(read_messages=False),
    	guild.me: discord.PermissionOverwrite(read_messages=True, embed_links=True, add_reactions=True),
		role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
	}		
	if msg.guild is None:
		try:
			if mod["Modmail"]["In Response"][str(ctx.author.id)] == True and mod["Modmail"]["On Going"][str(ctx.author.id)] != "On Ready":
				await msg.author.send("Please Wait For A Respond!")
				return

			
			elif mod["Modmail"]["On Going"][str(ctx.author.id)] == "On Ready":
				em=discord.Embed(
					description=msg.content,
					timestamp=datetime.now(),
					color=discord.Color.green()
				)

				for channel in guild.text_channels:
					if channel.topic == str(ctx.author.id):
						await channel.send(embed=em)
						break
			
			

		except KeyError:
			mod["Modmail"]["In Response"][str(ctx.author.id)] = {}
			mod["Modmail"]["In Response"][str(ctx.author.id)] = True
			mod["Modmail"]["On Going"][str(ctx.author.id)] = False
			with open("status.json", "w") as f:
				json.dump(mod,f,indent=4)
	
			if mod["Modmail"]["In Response"][str(ctx.author.id)] == True:
				em=discord.Embed(
					title=f"{ctx.author.id}",
					description=f"**🫂 Member :** {msg.author.name}\n**📬 Message :** {msg.content}",
					color=discord.Color.green()
				)


				channels=await cate.create_text_channel(name=f"Modmail- {ctx.author.name.title()}", topic=f"{ctx.author.id}", overwrites=Modmail)

				await channels.send(embed=em, content=ctx.author.id)
				await channels.send(f"{role.mention} Someone use the modmail system!")
				await ctx.author.send(f"Your requested has been fufilled :thumbsup:\nPlease wait until the MOD team response!")

				mod["Modmail"]["On Going"][str(ctx.author.id)] = True
				mod["Modmail"]["Channels"].append(str(channels.id))
				mod["Modmail"]["Members"].append(str(ctx.author.id))
				with open("status.json", "w") as f:
					json.dump(mod,f,indent=4)

			
				
	if str(msg.channel.id) in mod["Modmail"]["Channels"]:			
		Modmails = {
		ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: discord.PermissionOverwrite(read_messages=True, embed_links=True, add_reactions=True),
		role: discord.PermissionOverwrite(read_messages=True, send_messages=False, add_reactions=False, use_external_emojis=False)
	}
		if msg.content.startswith(f"help-"):
			help_=msg.content.lower().split("-")
			user=await client.fetch_user(int(help_[1]))
			if mod["Modmail"]["On Going"][str(user.id)] == True:
				mod["Modmail"]["On Going"][str(user.id)] = "On Ready"
				modmail[str(_id_)] = {}
				modmail[str(_id_)]["Name"] = user.name + '#' + user.discriminator
				modmail[str(_id_)]["Name Id"] = user.id
				modmail[str(_id_)]["Admin"] = ctx.author.id
				with open("status.json", "w") as f:
					json.dump(mod,f,indent=4)

				with open("modmail.json", "w") as f:
					json.dump(modmail,f,indent=4)

				em=discord.Embed(
					title="Modmail is active!",
					description=f"Your Modmail gonna be handle by **{msg.author.name}**",
					color=discord.Color.green()
				)

				ems=discord.Embed(
					title="Modmail is active!",
					description=f"Modmail Handle By **{ctx.author.name}**",
					color=discord.Color.green()
				)

				await user.send(embed=em)
				await ctx.send(embed=ems)
				await ctx.channel.edit(overwrites=Modmails)


			else:
				await ctx.send("The mod mail has been handle by someone else!")
				return

		elif msg.content.startswith("close"):
			em=discord.Embed(
				title="Modmail Close",
				description=f"Your modmail connection is close by **{msg.author.name}**",
				color=discord.Color.red()
			)
			await msg.channel.send("Closing this modmail in 5 seconds")
			user=await client.fetch_user(int(msg.channel.topic))
			mod["Modmail"]["Blacklist"].append(str(user.id))
			with open("status.json", "w") as f:
				json.dump(mod,f,indent=4)
			await user.send(embed=em)
			await asyncio.sleep(5)
			try:
				await msg.author.send(f"Succesfuly close **{msg.channel.name.split('-')[1].title()}**'s Modmail")
				mod["Modmail"]["Blacklist"].remove(str(user.id))
				mod["Modmail"]["Members"].remove(str(user.id))
				mod["Modmail"]["Channels"].remove(str(msg.channel.id))
				mod["Modmail"]["In Response"].pop(str(user.id))
				mod["Modmail"]["On Going"].pop(str(user.id))
				with open("status.json", "w") as f:
					json.dump(mod,f,indent=4)
				await msg.channel.delete()

			except Exception as e:
				raise e

		else:
			for m in mod["Modmail"]["Members"]:
				if mod["Modmail"]["On Going"][str(m)] == "On Ready":
					em=discord.Embed(
						description=msg.content,
						timestamp=datetime.now(),
						color=discord.Color.green()
					)

					user=await client.fetch_user(int(msg.channel.topic))
					await user.send(embed=em)
		
									 
									  
									  
@client.command(aliases=["bl"])
async def blacklist(ctx, m:discord.Member, *,reason="Not Provided"):
	if str(m.id) in mod["Modmail"]["Blacklist"]:
		await ctx.send(f"<@{m.id}> has already blacklist in the database")
		return
	try:
		mod["Modmail"]["Blacklist"].append(str(m.id))
		await ctx.send(f"{m.id} has been blacklisted")
		em=discord.Embed(
			title="Blacklisted!",
			description=f"You have been blacklisted!!\n**reason :** {reason}\nYour no longer can use this Modmail system!",
			color=discord.Color.red()
		)
		await m.send(embed=em,content="You\'ve Been Blacklisted With This Bot :)")
		with open("status.json", "w") as f:
			json.dump(mod,f,indent=4)
			
	except:
		await ctx.send("Wrong Member!\nMember Not Found :/")
									  
if __name__ == "__main__":
	client.run("YOUR TOKEN HERE")	
