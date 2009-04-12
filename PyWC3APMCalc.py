################################################################################
##Python Warcraft 3 APM Calculator v0.0000002
##  by John 'Erlog' Rozewicki
##   Based on work from w3g_format.txt and w3g_actions.txt
##
##     Don't bitch about the messiness of this. If it works, don't complain.
##                    I will make it prettier, I promise.
################################################################################
##Changelog
##v0.0000002 - Fixed a bug in my decoding of the encoded string.
##v0.0000001 - First release
################################################################################
import struct
import os
import zlib
#import pprint
import re
import inspect
import sys
from cStringIO import StringIO

from Tkinter import *
from tkMessageBox import *
from tkColorChooser import askcolor              
from tkFileDialog   import askopenfilename 


def main(fname, update):
	output = ''

	#Setup##########################################################################
	OutputString = StringIO()
	output += '\nPython Warcraft 3 APM Calculator\n     by John \'Erlog\' Rozewicki (jjrozewicki@gmail.com)\n\n'
	DecompressedData = ''
	HostRace = ''
	actionblock = ''
	actionblockpos = 0
	while True:
		try:
			ReplayPath = fname
			break
		except ValueError:
			output += "No such file. Check your path."

	Replay = open(ReplayPath, mode='rb')

	#PrettyPrinter = pprint.PrettyPrinter(indent=0)
	ReplayDataHead = []
	ActionDataHead = []
	DataPosition = 0
	size = 0
	Result = ["NOTEOF","NOTEOF"]

	################################################################################





	#Functions######################################################################
	def PullGameType(FirstPlayerRecordNull, EncodedStringNull):
		LsGameType = ["Type", "Flags"]
		GameType = GameTypeDict[struct.unpack_from('B', DecompressedData, EncodedStringNull+5)[0]]
		Flags = GameTypeDict[struct.unpack_from('B', DecompressedData, EncodedStringNull+6)[0]]
		LsGameType[0] = Flags
		LsGameType[1] = GameType
		return LsGameType

	def PullPlayerList(FirstPlayerRecordNull, EncodedStringNull):
		APMDictList = []
		FlatPlayerList = []
		PlayerListData = ''
		PlayerListStart = EncodedStringNull+13
		PlayerListData = DecompressedData[5:FirstPlayerRecordNull+2] + DecompressedData[EncodedStringNull+13:GameRecordStart]
		PlayerListData = PlayerListData.rsplit("\x16")
		for each in range(len(PlayerListData)):
			FlatPlayerList = FlatPlayerList + [[PlayerListData[each][0], PlayerListData[each][1:].rsplit("\x00")[0]]]
			APMDictList = APMDictList + [[PlayerListData[each][0], 0]]
		return dict(FlatPlayerList), dict(APMDictList)
		
	def checksum(st):
		return reduce(lambda x,y:x+y, map(ord, st))

	def int2bin(integer):
		#use ord to pass int from tuple
		bin = ''
		place = 128
		while place != 0:
			if integer & place == place:
				bin = bin + '1'
			else:
				bin = bin + '0'
			place = place/2
		bin = bin[::-1]	
		return bin
		
	def stringdecode(eTuple):
		eString = eTuple[0]
		dString = str()
		
		for x in range(0,(len(eString)/8)):
			StringSlice = eString[((x*8)):((x+1)*8)]
			ControlString = int2bin(ord(StringSlice[0]))
			for y in range(1,len(StringSlice)):
				if ControlString[y] == '0':
					dString = dString + chr(ord(StringSlice[y])-1)
					
				if ControlString[y] == '1':
					dString = dString + StringSlice[y]	
		return dString
		
	def ParseLeaveGame():
		localpos = DataPosition
		PlayerID = DecompressedData[localpos+5]
		APMDict[PlayerID] = APMDict[PlayerID]/(GameLength*((float(DataPosition)/float(len(DecompressedData)))+0.003))
		localpos = DataPosition + 14
		return ["ParseLeaveGame", localpos]
		
	def ParseTimeSlotBlock():
		ActionDataParser = {'\x01' : ParsePauseGame, '\x02' : ParseResumeGame, '\x03' : ParseSetSpeed, '\x04' : ParseIncreaseGameSpeed, '\x05' : ParseDecreaseGameSpeed, '\x06' : ParseSaveGame, '\x07' : ParseSaveGameFinished, '\x10' : ParseUseAbility, '\x11' : ParseUseAbilityPositionTargeted, '\x12' : ParseUseAbilityTargeted, '\x13' : ParseDropItem, '\x14' : ParseUseAbilityMultiTarget, '\x16' : ParseChangeSelection, '\x17' : ParseAssignGroupHotkey, '\x18' : ParseSelectGroupHotkey, '\x19' : ParseSelectSubgroup, '\x1a' : ParsePreSubSelection, '\x1b' : ParseUnknown1, '\x1c' : ParseSelectGroundItem, '\x1d' : ParseCancelHeroRevival, '\x1e' : ParseRemoveUnitFromBuildingQueue, '\x21' : ParseUnknown9, '\x20' : ParseCheatFastCooldown, '\x22' : ParseCheatInstantDefeat, '\x23' : ParseCheatSpeedConstruction, '\x24' : ParseCheatFastDeath, '\x25' : ParseCheatRemoveFoodLimit, '\x26' : ParseCheatGodMode, '\x27' : ParseCheatGold, '\x28' : ParseCheatLumber, '\x29' : ParseCheatMana, '\x2a' : ParseCheatNoDefeat, '\x2b' : ParseCheatVictoryConditions, '\x2c' : ParseCheatEnableResearch, '\x2d' : ParseCheatGoldLumber, '\x2e' : ParseCheatTimeOfDay, '\x2f' : ParseCheatFogOfWar, '\x30' : ParseCheatTechTree, '\x31' : ParseCheatResearchUpgrades, '\x32' : ParseCheatInstantVictory, '\x50' : ParseChangeAllyOptions, '\x51' : ParseTransferResources, '\x60' : ParseMapTriggerChatCommand, '\x61' : ParseEsc, '\x62' : ParseScenarioTrigger, '\x66' : ParseHeroChooseSkillSubmenu, '\x67' : ParseChooseBuildingSubmenu, '\x68' : ParseMinimapSignal, '\x69' : ParseContinueGameBlockB, '\x6a' : ParseContinueBlockA, '\x75' : Unknown2}
		APMActionDatabase= {"ParsePauseGame" : 0, "ParseResumeGame" : 0, "ParseSetSpeed" : 0, "ParseIncreaseGameSpeed" : 0, "ParseDecreaseGameSpeed" : 0, "ParseSaveGame" : 0, "ParseSaveGameFinished" : 0, "ParseUseAbility" : 1, "ParseUseAbilityPositionTargeted" : 1, "ParseUseAbilityTargeted" : 1, "ParseDropItem" : 1, "ParseUseAbilityMultiTarget" : 1, "ParseChangeSelection" : 1, "ParseAssignGroupHotkey" : 1, "ParseSelectGroupHotkey" : 1, "ParseSelectSubgroup" : 1, "ParsePreSubSelection" : 0, "ParseUnknown1" : 0, "ParseSelectGroundItem" : 1, "ParseCancelHeroRevival" : 1, "ParseRemoveUnitFromBuildingQueue" : 1, "ParseUnknown9" : 0, "ParseCheatFastCooldown" : 0, "ParseCheatInstantDefeat" : 0, "ParseCheatSpeedConstruction" : 0, "ParseCheatFastDeath" : 0, "ParseCheatRemoveFoodLimit" : 0, "ParseCheatGodMode" : 0, "ParseCheatGold" : 0, "ParseCheatLumber" : 0, "ParseCheatMana" : 0, "ParseCheatNoDefeat" : 0, "ParseCheatVictoryConditions" : 0, "ParseCheatEnableResearch" : 0, "ParseCheatGoldLumber" : 0, "ParseCheatTimeOfDay" : 0, "ParseCheatFogOfWar" : 0, "ParseCheatTechTree" : 0, "ParseCheatResearchUpgrades" : 0, "ParseCheatInstantVictory" : 0, "ParseChangeAllyOptions" : 0, "ParseTransferResources" : 1, "ParseMapTriggerChatCommand" : 0, "ParseEsc" : 1, "ParseScenarioTrigger" : 0, "ParseHeroChooseSkillSubmenu" : 1, "ParseChooseBuildingSubmenu" : 1, "ParseMinimapSignal" : 1, "ParseContinueGameBlockB" : 0, "ParseContinueBlockA" : 0, "Unknown2" : 0}
		ActionDataHead = ''
		PlayerID = ''
		actionblockpos = 0
		actionblock = ''
		endofblock = 0
		actionblocksize = 0
		localpos = DataPosition + 1
		size = struct.unpack_from('H', DecompressedData, localpos)
		endofblock = localpos + size[0] + 2
		localpos = localpos+4
		if size[0] > 2:
			PlayerID = DecompressedData[localpos]
			actionblockend = struct.unpack_from('H', DecompressedData, localpos+1)[0] + localpos + 1
			actionblock = struct.unpack_from('%is' % (actionblockend-localpos-1), DecompressedData, localpos+3)[0]
			while actionblockpos < len(actionblock):
				ActionDataHead = struct.unpack_from('c', actionblock, actionblockpos)
				Result = ActionDataParser[ActionDataHead[0]](actionblock,actionblockpos)
				actionblockpos = Result[1]
				APMDict[PlayerID] = APMDict[PlayerID]+APMActionDatabase[Result[0]]
		return ["TimeSlotBlock", endofblock]
		
	def ParseChatMessage():
		localpos = DataPosition + 2
		size = struct.unpack_from('H', DecompressedData, localpos)
		localpos = localpos + size[0] + 2
		return ["ParseChatMessage", localpos]
		
	def ParseChecksum():
		localpos = DataPosition + 1
		size = struct.unpack_from('B', DecompressedData, localpos)
		localpos = localpos + size[0] + 1
		return ["ParseChecksum", localpos]
		
	def ParseUnknown():
		localpos = DataPosition + 11
		return ["ParseUnknown", localpos]
	def ParseEndGameCountdown():
		localpos = DataPosition + 9
		return ["ParseEndGameCountdown", localpos]
	def EndOfFile():
		localpos = DataPosition+1
		return ["EOF", localpos]
	################################################################################


	#Parsing Actions################################################################
	def ParsePauseGame(actionblock, actionblockpos):
		localpos = actionblockpos + 2
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseResumeGame(actionblock, actionblockpos):
		localpos = actionblockpos + 2
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseSetSpeed(actionblock, actionblockpos):
		localpos = actionblockpos + 2
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseIncreaseGameSpeed(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseDecreaseGameSpeed(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseSaveGame(actionblock, actionblockpos):
		localpos = actionblockpos
		localpos = localpos + len(actionblock) + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseSaveGameFinished(actionblock, actionblockpos):
		localpos = actionblockpos + 6
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseUseAbility(actionblock, actionblockpos):
		localpos = actionblockpos + 15
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseUseAbilityPositionTargeted(actionblock, actionblockpos):
		localpos = actionblockpos + 24
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseUseAbilityTargeted(actionblock, actionblockpos):
		localpos = actionblockpos + 31
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseDropItem(actionblock, actionblockpos):
		localpos = actionblockpos + 39
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseUseAbilityMultiTarget(actionblock, actionblockpos):
		localpos = actionblockpos + 44
		return ["%s" % inspect.stack()[0][3], localpos]
		
	#variable
	def ParseChangeSelection(actionblock, actionblockpos):
		localpos = actionblockpos + 2	
		NumberOfBuildings = struct.unpack_from('H', actionblock, localpos)
		localpos = localpos+2+(NumberOfBuildings[0]*8)
		return ["%s" % inspect.stack()[0][3], localpos]
		
	def ParseAssignGroupHotkey(actionblock, actionblockpos):
		localpos = actionblockpos + 2	
		NumberOf = struct.unpack_from('H', actionblock, localpos)
		#print NumberOf
		localpos = localpos+2+(NumberOf[0]*8)
		return ["%s" % inspect.stack()[0][3], localpos]

	def ParseSelectGroupHotkey(actionblock, actionblockpos):
		localpos = actionblockpos + 3
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseSelectSubgroup(actionblock, actionblockpos):
		localpos = actionblockpos + 13
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParsePreSubSelection(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseUnknown1(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseSelectGroundItem(actionblock, actionblockpos):
		localpos = actionblockpos + 10
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCancelHeroRevival(actionblock, actionblockpos):
		localpos = actionblockpos + 9
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseRemoveUnitFromBuildingQueue(actionblock, actionblockpos):
		localpos = actionblockpos + 6
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseUnknown9(actionblock, actionblockpos):
		localpos = actionblockpos + 9
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatFastCooldown(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatInstantDefeat(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatSpeedConstruction(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatFastDeath(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatRemoveFoodLimit(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatGodMode(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatGold(actionblock, actionblockpos):
		localpos = actionblockpos + 6
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatLumber(actionblock, actionblockpos):
		localpos = actionblockpos + 6
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatMana(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatNoDefeat(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatVictoryConditions(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatEnableResearch(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatGoldLumber(actionblock, actionblockpos):
		localpos = actionblockpos + 6
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatTimeOfDay(actionblock, actionblockpos):
		localpos = actionblockpos + 5
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatFogOfWar(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatTechTree(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatResearchUpgrades(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseCheatInstantVictory(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseChangeAllyOptions(actionblock, actionblockpos):
		localpos = actionblockpos + 6
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseTransferResources(actionblock, actionblockpos):
		localpos = actionblockpos + 10
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseMapTriggerChatCommand(actionblock, actionblockpos):
	#####null terminated string
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseEsc(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseScenarioTrigger(actionblock, actionblockpos):
		localpos = actionblockpos + 13
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseHeroChooseSkillSubmenu(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseChooseBuildingSubmenu(actionblock, actionblockpos):
		localpos = actionblockpos + 1
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseMinimapSignal(actionblock, actionblockpos):
		localpos = actionblockpos + 13
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseContinueGameBlockB(actionblock, actionblockpos):
		localpos = actionblockpos + 17
		return ["%s" % inspect.stack()[0][3], localpos]
	def ParseContinueBlockA(actionblock, actionblockpos):
		localpos = actionblockpos + 17
		return ["%s" % inspect.stack()[0][3], localpos]
	def Unknown2(actionblock, actionblockpos):
		localpos = actionblockpos + 2
		return ["%s" % inspect.stack()[0][3], localpos]
	################################################################################




	#Dictionaries###################################################################
	ExpansionDict = {"3RAW" : "Reign of Chaos", "PX3W" : "Frozen Throne"}
	GameTypeDict = {0 : "Public", 1 : "Ladder", 8 : "Private", 9 : "Custom", 13 : "Single Player", 32 : "Ladder Team"}
	RaceDict = {(1,) : "Human", (2,) : "Orc", (4,) : "Night Elf", (8,) : "Undead", (32,) : "Random", (10,) : "Daemon", (40,) : "Selectable"}
	GameSpeedDict = {'\x00' : "Slow", '\x01' : "Normal", '\x02' : "Fast"}
	ReplayDataParser = {'\x00' : EndOfFile, '\x17' : ParseLeaveGame, '\x1f' : ParseTimeSlotBlock, '\x20' : ParseChatMessage, '\x22' : ParseChecksum, '\x23' : ParseUnknown, '\x2f' : ParseEndGameCountdown}
	################################################################################





	#Read Header Info###############################################################
	FirstString = Replay.read(28)
	if FirstString != "Warcraft III recorded game\x1a\x00":
		output += "Not a valid replay."
		quit()
	Header = struct.unpack('LLLLL', Replay.read(20))
	Subheader = struct.unpack('4sLHHLL', Replay.read(20))
	################################################################################





	#Decompress all data blocks to str#############################################
	for x in range(0, Header[4]):
		Decompressor = zlib.decompressobj()
		DataBlockHeader = struct.unpack('HHL', Replay.read(8))
		CompressedData = Replay.read(DataBlockHeader[0])
		DecompressedData = DecompressedData + Decompressor.decompress(CompressedData)
		Decompressor.flush()
		del Decompressor
	################################################################################






	#ParseHeaders####################################################################
	FirstPlayerRecordNull = DecompressedData.find("\0",6)
	GameNameNull = DecompressedData.find("\0",FirstPlayerRecordNull+12)
	EncodedStringNull = DecompressedData.find('\0',GameNameNull+2)
	GameRecordStart = DecompressedData.find("\x1a\x01\x00\x00\x00\x1b\x01\x00\x00\x00\x1c\x01\x00\x00\x00",EncodedStringNull+13)+15
	PlayerListDict, APMDict = PullPlayerList(FirstPlayerRecordNull, EncodedStringNull)
	GameLength = float(Subheader[4])/60000
	GameType = PullGameType(FirstPlayerRecordNull, EncodedStringNull)
	NumberOfSlots = ord(struct.unpack_from('c', DecompressedData, GameRecordStart+3)[0])
	SlotRecords = struct.unpack_from('%ic' % 9*NumberOfSlots,DecompressedData, GameRecordStart+4)

	DataPosition = GameRecordStart
	################################################################################



	#Encoded String#################################################################
	eString = struct.unpack_from("%is" % (EncodedStringNull-(GameNameNull+2)),DecompressedData,GameNameNull+2)
	dString = stringdecode(eString)
	GameSettings = struct.unpack_from("cccccccccL",dString)
	MapNameNull = dString.find('\0',13)
	MapName = struct.unpack_from("%is" % (MapNameNull-13),dString,13)
	CreatorNameNull = dString.find('\0', MapNameNull+1)
	CreatorName = struct.unpack_from("%is" % (CreatorNameNull-MapNameNull-1),dString,MapNameNull+1)
	GameSpeed = GameSpeedDict[GameSettings[0]]
	################################################################################



	####Decompress and Parse Replay Data############################################
	#print struct.unpack_from('100c', DecompressedData, 1647546)

	#print len(DecompressedData)
	counter = 0
	while DataPosition != len(DecompressedData):
		counter += 1
		if not (counter % 100):
			update()
		#print DataPosition
		ReplayDataHead = struct.unpack_from('c', DecompressedData, DataPosition)
		#print ReplayDataHead
		Result = ReplayDataParser[ReplayDataHead[0]]()
		DataPosition = Result[1]
		#if Result[0] != "EOF":
			#ParsedData.write(Result[0]+'\n')
	#ParsedData.write("EOF\n")
	################################################################################

	#Output##################################################################################
	#OutputString.write(FirstString+'\n')
	OutputString.write('Version: 1.%i.%i\n' % (Subheader[1],Subheader[2]))
	OutputString.write('Game Type: '+GameType[0]+' '+GameType[1]+' Game\n')
	OutputString.write('Game Speed: '+GameSpeed+'\n')
	OutputString.write('Game Length: '+str(GameLength)+' minutes \n')
	OutputString.write('Creator: '+CreatorName[0]+'\n')
	OutputString.write('Map: '+MapName[0]+'\n')
	for each in range(len(PlayerListDict)):
		if APMDict[PlayerListDict.items()[each][0]] > 5:
			if str(PlayerListDict.items()[each][1]) == '':
				OutputString.write("    Player "+str(each+1)+": "+str(APMDict[PlayerListDict.items()[each][0]])+"\n")
			else:	
				OutputString.write("    "+str(PlayerListDict.items()[each][1])+": "+str(APMDict[PlayerListDict.items()[each][0]])+"\n")
		
	output += OutputString.getvalue()	
	################################################################################


	#Cleanup########################################################################
	Replay.close()
	################################################################################

	return output

"""
Busybar widget
Rick Lawson
r_b_lawson at yahoo dot com
Heavily borrowed from ProgressBar.py which I got off the net but can't remember where
Feel free to add credits.
Comments by Stewart Midwinter: 
 I added a Quit button so you can stop the app.
 I also set up a timer so that the BusyBar stops after a certain period.
 Next, I added a button to bring up a BusyBar in a top-level window, similar to what
 you might a process to do while it was, in fact, busy.
 The top-level window is non-modal; it's left as an exercise for you, the reader, to change that if needed.


config options
--------------
BusyBar is derived from frame so all frame options are fine
Here are the options specific to this widget
fill       - color of the progress box (the box that bounces back and forth)
boxWidth   - width of progress box as a fraction of total widget width
interval   - interval in ms at which the progress box is moved
             ie, the shorter this is the faster the box will move
increment  - fraction of widget width that the box moves during an update
             ie, 0.05 means that box will move 5% of the total width at an update
text       - text of message that is displayed in the middle of the widget
foreground - color of text message
font       - font of text message
"""
def pop(dict, key, default):
    value = dict.get(key, default)
    if dict.has_key(key):
        del dict[key]
    return value

class BusyBar(Frame):
    def __init__(self, master=None, **options):
        # make sure we have sane defaults
        self.master=master
        self.options=options
        self.width=options.setdefault('width', 100)
        self.height=options.setdefault('height', 10)
        self.background=options.setdefault('background', 'gray')
        self.relief=options.setdefault('relief', 'sunken')
        self.bd=options.setdefault('bd', 2)

        #extract options not applicable to frames
        self._extractOptions(options)

        # init the base class
        Frame.__init__(self, master, options)

        self.incr=self.width*self.increment
        self.busy=0
        self.dir='right'

        # create the canvas which is the container for the bar
        self.canvas=Canvas(self, height=self.height, width=self.width, bd=0,
                           highlightthickness=0, background=self.background)
        # catch canvas resizes
        self.canvas.bind('<Configure>', self.onSize)

        # this is the bar that moves back and forth on the canvas
        self.scale=self.canvas.create_rectangle(0, 0, self.width*self.barWidth, self.height, fill=self.fill)

        # label that is in the center of the widget
        self.label=self.canvas.create_text(self.canvas.winfo_reqwidth() / 2,
                                           self.height / 2, text=self.text,
                                           anchor="c", fill=self.foreground,
                                           font=self.font)
        self.update()
        self.canvas.pack(side=TOP, fill=X, expand=NO)

    def _extractOptions(self, options):
        # these are the options not applicable to a frame
        self.foreground=pop(options, 'foreground', 'yellow')
        self.fill=pop(options, 'fill', 'blue')
        self.interval=pop(options, 'interval', 30)
        self.font=pop(options, 'font','helvetica 10')
        self.text=pop(options, 'text', '')
        self.barWidth=pop(options, 'barWidth', 0.2)
        self.increment=pop(options, 'increment', 0.05)

    # todo - need to implement config, cget, __setitem__, __getitem__ so it's more like a reg widget
    # as it is now, you get a chance to set stuff at the constructor but not after

    def onSize(self, e=None):
        self.width = e.width
        self.height = e.height
        # make sure the label is centered
        self.canvas.delete(self.label)
        self.label=self.canvas.create_text(self.width / 2, self.height / 2, text=self.text,
                                           anchor="c", fill=self.foreground, font=self.font)

    def on(self):
        self.busy = 1
        self.canvas.after(self.interval, self.update)

    def of(self):
        self.busy = 0

    def update(self):
        # do the move
        x1,y1,x2,y2 = self.canvas.coords(self.scale)
        if x2>=self.width:
            self.dir='left'
        if x1<=0:
            self.dir='right'
        if self.dir=='right':
            self.canvas.move(self.scale, self.incr, 0)
        else:
            self.canvas.move(self.scale, -1*self.incr, 0)

        if self.busy:
            self.canvas.after(self.interval, self.update)
        self.canvas.update_idletasks()

import os.path

class Interface:
    def __init__(self, master):
        self.master = master
        try:
            f = open(os.path.join(os.path.expanduser('~'), '.pywc3apmcalc'))
            self.last_used_dir = f.read()
        except:
            self.last_used_dir = None
        frame = Frame(master)
        frame.pack()
        self.open_button = Button(frame, text="Open", command=self.open_dialog)
        self.open_button.pack()
        self.output_text = Text(master, state=DISABLED)
        self.output_text.pack()

        if len(sys.argv) > 1:
            self.open(sys.argv[1])


    def updater(self, bb1):
        bb1.update()
        self.master.update()
        
    def open_dialog(self):
        fname = askopenfilename(initialdir=self.last_used_dir)
        if not fname:
            return
        self.open(fname)

    def open(self, fname):
        self.last_used_dir = os.path.dirname(fname)
        try:
            open(os.path.join(os.path.expanduser('~'), '.pywc3apmcalc'), 'w').write(self.last_used_dir)
        except:
            pass
        bb1=BusyBar(self.master, text='Processing ...')
        bb1.pack()

        self.open_button.config(state=DISABLED)
        output = main(fname, lambda: self.updater(bb1))
        self.open_button.config(state=NORMAL)

        bb1.of()
        bb1.destroy()

        self.output_text.config(state=NORMAL)
        self.output_text.delete(1.0, END)
        self.master.title('PyWC3APMCalc - ' + os.path.basename(fname))
        self.output_text.insert(END, output)
        self.output_text.config(state=DISABLED)


root = Tk()
root.title('PyWC3APMCalc')
root.resizable(width = False, height = False)
interface = Interface(root)
root.mainloop()
