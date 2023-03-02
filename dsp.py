# coding: utf-8

from pathlib import Path
from crystal_tts import Mimic3Settings
from crystal_tts.speechplayer import CrystalSpeechPlayer


SSML = """
<speak>
<s>ABSTRACT:</s>
<break value="300ms"/>
<s>
This research aims to assess the determinants of the financial risk of commercial banks in Sudan.
</s>
<break value="300ms"/>
<s>
It uses value at risk (VaR) technique to estimate the expected losses in banks' profitability, then it investigates the determinants of financial risk by considering both bank specific as well as macroeconomic variables using panel data regression model.
</s>
<break value="300ms"/>
<s>
The bank specific variables are the banks investments as measured by the total assets, and the bank size as measured by total deposits. While the inflation rate is the macroeconomic factor.
</s>
<break value="300ms"/>
<s>
The sample includes thirteen banks during the period from 2012 to 2020. The findings of the study reveal that the VaR estimates for the banks in the sample range from 1% to 5% at 5 percent confidence level.
</s>
<break value="300ms"/>
<s>
This implies that the expected profitability loses of banks range from about 0.5 million SDG to 79 million SDG for other banks under normal conditions.
</s>
<break value="300ms"/>
<s>
On the other hand the regression results show significant positive association between the financial risk and the investment variable while the relation between the financial risk of banks and both the banks' size and the inflation rate is significantly negative.
</s>
</speak>
"""


CRYSTALTTS_DATA_PATH = Path.home().joinpath("crystal_tts", "voices")
CRYSTALTTS_DATA_PATH.mkdir(exist_ok=True)
tts_settings = Mimic3Settings(
    voice="",
    language="",
    voices_directories=[CRYSTALTTS_DATA_PATH],
    sample_rate=16000
)


player = CrystalSpeechPlayer(tts_settings)
#player.tts.voice = "en_US/ryan_low"
player.speak_ssml(SSML)
