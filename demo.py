# coding: utf-8

from pathlib import Path
from crystal_tts import Mimic3Settings, Mimic3TextToSpeechSystem, SSMLSpeaker

TEXT = """
ABSTRACT: This research aims to assess the determinants of the financial risk of commercial banks in Sudan. It uses value at risk (VaR) technique to estimate the expected losses in banks' profitability, then it investigates the determinants of financial risk by considering both bank specific as well as macroeconomic variables using panel data regression model. The bank specific variables are the banks investments as measured by the total assets, and the bank size as measured by total deposits. While the inflation rate is the macroeconomic factor. The sample includes thirteen banks during the period from 2012 to 2020. The findings of the study reveal that the VaR estimates for the banks in the sample range from 1% to 5% at 5 percent confidence level. This implies that the expected profitability loses of banks range from about 0.5 million SDG to 79 million SDG for other banks under normal conditions. On the other hand the regression results show significant positive association between the financial risk and the investment variable while the relation between the financial risk of banks and both the banks' size and the inflation rate is significantly negative. These findings implies that larger banks are less subject to financial risk than smaller banks, more over banks investments increase their financial risk .on the other hand , as inflation rate increase the financial risk decreases.
"""
CRYSTALTTS_DATA_PATH = Path.home().joinpath("crystal_tts", "voices")
CRYSTALTTS_DATA_PATH.mkdir(exist_ok=True)


tts_settings = Mimic3Settings(
    voice="",
    language="",
    voices_directories=[CRYSTALTTS_DATA_PATH]
)

tts = Mimic3TextToSpeechSystem(tts_settings)
print(list(tts.get_voices()))
tts.voice = "en_US/ryan_low"
res = tts.text_to_wav(TEXT)
with open("out.wav", "wb") as file:
    file.write(res)
