import os
import zlib
from collections import namedtuple
from source.reaper import Reaper, file_reaper
from source.codecs.zip_methods import ZipMethods


class ReEngine(Reaper):
    game_file_list = None
    game = None

    @file_reaper
    def run(self):

        with open(self.file_name, "rb") as file:
            magic = file.read(4)
            print(self.game, self.game, self.game_file_list)

            if not self.magic([b'KPKA', ], magic, 'Capcom ReEngine PAK Archive'):
                return

            version = int.from_bytes(file.read(4), byteorder="little")
            file_count = int.from_bytes(file.read(4), byteorder="little")
            FileList = namedtuple('FileList',
                                  ['name_hash', 'offset', 'zip_size', 'unzip_size', 'index'])
            file_list = []
            
            if self.game is not None:
                self.game_file_list = game_list.get(self.game)

            if self.game_file_list is not None:

                with open('data\\re_list\\' + self.game_file_list, 'rb') as gl:
                    file_name_list = zlib.decompress(gl.read()).decode('utf-8').split('\n')

            else:
                file_name_list = []

            print(self.game, self.game, self.game_file_list)

            for i in range(file_count):

                name_hash = file.read(0xC if i == 0 else 0x10)
                offset = int.from_bytes(file.read(8), byteorder="little")
                zip_size = int.from_bytes(file.read(8), byteorder="little")
                unzip_size = int.from_bytes(file.read(8), byteorder="little")
                index = int.from_bytes(file.read(8), byteorder="little")

                file_list.append(FileList(name_hash, offset, zip_size, unzip_size, index))

            for j, file_info in enumerate(file_list):

                try:
                    file_name = file_name_list[file_info.index].strip()
                    ext = file_name.split('.')[-1]

                    try:
                        int(ext)
                        file_name = file_name.replace(f'.{ext}', '')
                    except ValueError:
                        pass

                except IndexError:
                    file_name = str(int.from_bytes(file_info.name_hash)) + '.dat'

                path = os.path.join(self.output_folder, file_name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                file.seek(file_info.offset)
                self.file_save(path, file.read(file_info.zip_size))
                self.unzip(path, ZipMethods.DEFLATE_NOERROR)
                self.update_pb(file_count, j + 1, file_name)


game_list = {
    "Apollo Justice: Ace Attorney Trilogy (Nintendo Switch)": "AJ_AAT_NSW_Release.list",
    "Apollo Justice: Ace Attorney Trilogy (PC Steam)": "AJ_AAT_PC_Release.list",
    "Apollo Justice: Ace Attorney Trilogy (PlayStation 4)": "AJ_AAT_PS4_Release.list",
    "Biohazard 2 Remake (MS Store)": "RE2_MSG_Release.list",
    "Biohazard 2 Remake (PC Steam)": "RE2_PC_Release.list",
    "Biohazard 2 Remake (PlayStation 4)": "RE2_PS4_Release.list",
    "Biohazard 2 Remake (RT) (PC Steam)": "RE2_RT_PC_Release.list",
    "Biohazard 2: 1-Shot Demo (PC Steam)": "RE2_1S_PC_Demo.list",
    "Biohazard 2: 1-Shot Demo (PlayStation 4)": "RE2_1S_PS4_Demo.list",
    "Biohazard 2: R.P.D. Demo (PC Steam)": "RE2_RPD_PC_Demo.list",
    "Biohazard 2: Z Version (RT) (PC Steam)": "RE2Z_RT_PC_Release.list",
    "Biohazard 3 Remake (MS Store)": "RE3_MSG_Release.list",
    "Biohazard 3 Remake (PC Steam)": "RE3_PC_Release.list",
    "Biohazard 3 Remake (PlayStation 4)": "RE3_PS4_Release.list",
    "Biohazard 3 Remake (RT) (PC Steam)": "RE3_RT_PC_Release.list",
    "Biohazard 3: Raccoon City Demo (PC Steam)": "RE3_RC_PC_Demo.list",
    "Biohazard 3: Raccoon City Demo (PlayStation 4)": "RE3_RC_PS4_Demo.list",
    "Biohazard 3: Z Version (RT) (PC Steam)": "RE3Z_RT_PC_Release.list",
    "Biohazard 4 Remake (Encrypted) (PC Steam)": "RE4_PC_Release.list",
    "Biohazard 4 Remake (MacOS)": "RE4_MAC_Release.list",
    "Biohazard 4 Remake (PlayStation 4)": "RE4_PS4_Release.list",
    "Biohazard 4: Chainsaw Demo (PC Steam)": "RE4_PC_Demo.list",
    "Biohazard 7: Gold Edition (PlayStation 4)": "RE7_GE_PS4_Release.list",
    "Biohazard 7: Kitchen Demo (PlayStation 4)": "RE7_K_PS4_Demo.list",
    "Biohazard 7: Resident Evil (PC Steam)": "RE7_PC_Release.list",
    "Biohazard 7: Resident Evil (PlayStation 4)": "RE7_PS4_Release.list",
    "Biohazard 7: Resident Evil (RT) (PC Steam)": "RE7_RT_PC_Release.list",
    "Biohazard 7: Resident Evil Z Version (PC Steam)": "RE7Z_PC_Release.list",
    "Biohazard 7: Teaser - Beginning Hour (MS Store)": "RE7_TBH_UWP_Demo.list",
    "Biohazard 7: Teaser - Beginning Hour (PC Steam)": "RE7_TBH_PC_Demo.list",
    "Biohazard 7: Teaser - Beginning Hour (PlayStation 4)": "RE7_TBH_PS4_Demo.list",
    "Biohazard 8: Village (iOS)": "RE8_iOS_Release.list",
    "Biohazard 8: Village (MacOS)": "RE8_MAC_Release.list",
    "Biohazard 8: Village (PC Steam)": "RE8_PC_Release.list",
    "Biohazard 8: Village Gameplay Demo (PC Steam)": "RE8_PC_Demo.list",
    "Biohazard 8: Village Gameplay Demo (PlayStation 4)": "RE8_PS4_Demo.list",
    "Biohazard 8: Village Gold Edition Gameplay Demo (PC Steam)": "RE8_PC_Demo_Gold.list",
    "Biohazard 8: Village Maiden Demo (PlayStation 5)": "RE8_M_PS5_Demo.list",
    "Biohazard 8: Village Z Version (PC Steam)": "RE8Z_PC_Release.list",
    "Biohazard: Re:Verse (Open Beta) (PC Steam)": "RERE_PC_Open_Beta.list",
    "Biohazard: Re:Verse (PC Steam)": "RERE_PC_Release.list",
    "Biohazard: Re:Verse (PlayStation 4)": "RERE_PS4_Release.list",
    "Biohazard: Resistance (Open Beta) (PC Steam)": "RER_PC_Open_Beta.list",
    "Biohazard: Resistance (PC Steam)": "RER_PC_Release.list",
    "Capcom Arcade 2nd Stadium (Nintendo Switch)": "CAS2_NSW_Release.list",
    "Capcom Arcade 2nd Stadium (PC Steam)": "CAS2_PC_Release.list",
    "Capcom Arcade 2nd Stadium (PlayStation 4)": "CAS2_PS4_Release.list",
    "Capcom Arcade Stadium (Nintendo Switch)": "CAS_NSW_Release.list",
    "Capcom Arcade Stadium (PC Steam)": "CAS_PC_Release.list",
    "Capcom Arcade Stadium (PlayStation 4)": "CAS_PS4_Release.list",
    "Dead Rising Deluxe Remaster (PC Steam)": "DRDR_PC_Release.list",
    "Devil May Cry 5 (PC Steam)": "DMC5_PC_Release.list",
    "Devil May Cry 5 (PlayStation 4)": "DMC5_PS4_Release.list",
    "Dragon's Dogma 2 - Character Creator & Storage Demo (PC Steam)": "DD2CCS_PC_Demo.list",
    "Dragon's Dogma 2 (PC Steam)": "DD2_PC_Release.list",
    "Exoprimal (Closed Beta) (PC Steam)": "EXP_PC_Closed_Beta.list",
    "Exoprimal (PC Steam)": "EXP_PC_Release.list",
    "Ghost Trick: Phantom Detective (Nintendo Switch)": "GTPD_NSW_Release.list",
    "Ghost Trick: Phantom Detective (PC Steam)": "GTPD_PC_Release.list",
    "Ghost Trick: Phantom Detective (PlayStation 4)": "GTPD_PS4_Release.list",
    "Ghost Trick: Phantom Detective Demo (Nintendo Switch)": "GTPD_NSW_Demo.list",
    "Ghost Trick: Phantom Detective Demo (PC Steam)": "GTPD_PC_Demo.list",
    "Ghosts 'n Goblins Resurrection (Nintendo Switch)": "GGR_NSW_Release.list",
    "Ghosts 'n Goblins Resurrection (PC Steam)": "GGR_PC_Release.list",
    "Ghosts 'n Goblins Resurrection (PlayStation 4)": "GGR_PS4_Release.list",
    "Kunitsu-Gami: Path of the Goddess - Demo (PC Steam)": "KGPG_PC_Demo.list",
    "Kunitsu-Gami: Path of the Goddess (MS Store)": "KGPG_MSG_Release.list",
    "Kunitsu-Gami: Path of the Goddess (PC Steam)": "KGPG_PC_Release.list",
    "MONSTER HUNTER RISE (Encrypted) (PC Steam)": "MHR_PC_Release.list",
    "MONSTER HUNTER RISE (MS Store)": "MHR_MSG_Release.list",
    "MONSTER HUNTER RISE (Nintendo Switch)": "MHR_NSW_Release.list",
    "MONSTER HUNTER RISE DEMO (PC Steam)": "MHR_PC_Demo.list",
    "MONSTER HUNTER RISE: SUNBREAK DEMO (Encrypted) (PC Steam)": "MHRS_PC_Demo.list",
    "Resident Evil 2 Remake (MS Store)": "RE2_MSG_Release.list",
    "Resident Evil 2 Remake (PC Steam)": "RE2_PC_Release.list",
    "Resident Evil 2 Remake (PlayStation 4)": "RE2_PS4_Release.list",
    "Resident Evil 2 Remake (RT) (PC Steam)": "RE2_RT_PC_Release.list",
    "Resident Evil 2: 1-Shot Demo (PC Steam)": "RE2_1S_PC_Demo.list",
    "Resident Evil 2: 1-Shot Demo (PlayStation 4)": "RE2_1S_PS4_Demo.list",
    "Resident Evil 2: R.P.D. Demo (PC Steam)": "RE2_RPD_PC_Demo.list",
    "Resident Evil 2: Z Version (RT) (PC Steam)": "RE2Z_RT_PC_Release.list",
    "Resident Evil 3 Remake (MS Store)": "RE3_MSG_Release.list",
    "Resident Evil 3 Remake (PC Steam)": "RE3_PC_Release.list",
    "Resident Evil 3 Remake (PlayStation 4)": "RE3_PS4_Release.list",
    "Resident Evil 3 Remake (RT) (PC Steam)": "RE3_RT_PC_Release.list",
    "Resident Evil 3: Raccoon City Demo (PC Steam)": "RE3_RC_PC_Demo.list",
    "Resident Evil 3: Raccoon City Demo (PlayStation 4)": "RE3_RC_PS4_Demo.list",
    "Resident Evil 3: Z Version (RT) (PC Steam)": "RE3Z_RT_PC_Release.list",
    "Resident Evil 4 Remake (Encrypted) (PC Steam)": "RE4_PC_Release.list",
    "Resident Evil 4 Remake (MacOS)": "RE4_MAC_Release.list",
    "Resident Evil 4 Remake (PlayStation 4)": "RE4_PS4_Release.list",
    "Resident Evil 4: Chainsaw Demo (PC Steam)": "RE4_PC_Demo.list",
    "Resident Evil 7: Biohazard (PC Steam)": "RE7_PC_Release.list",
    "Resident Evil 7: Biohazard (PlayStation 4)": "RE7_PS4_Release.list",
    "Resident Evil 7: Biohazard (RT) (PC Steam)": "RE7_RT_PC_Release.list",
    "Resident Evil 7: Biohazard Z Version (PC Steam)": "RE7Z_PC_Release.list",
    "Resident Evil 7: Gold Edition (PlayStation 4)": "RE7_GE_PS4_Release.list",
    "Resident Evil 7: Kitchen Demo (PlayStation 4)": "RE7_K_PS4_Demo.list",
    "Resident Evil 7: Teaser - Beginning Hour (MS Store)": "RE7_TBH_UWP_Demo.list",
    "Resident Evil 7: Teaser - Beginning Hour (PC Steam)": "RE7_TBH_PC_Demo.list",
    "Resident Evil 7: Teaser - Beginning Hour (PlayStation 4)": "RE7_TBH_PS4_Demo.list",
    "Resident Evil 8: Village (iOS)": "RE8_iOS_Release.list",
    "Resident Evil 8: Village (MacOS)": "RE8_MAC_Release.list",
    "Resident Evil 8: Village (PC Steam)": "RE8_PC_Release.list",
    "Resident Evil 8: Village Gameplay Demo (PC Steam)": "RE8_PC_Demo.list",
    "Resident Evil 8: Village Gameplay Demo (PlayStation 4)": "RE8_PS4_Demo.list",
    "Resident Evil 8: Village Gold Edition Gameplay Demo (PC Steam)": "RE8_PC_Demo_Gold.list",
    "Resident Evil 8: Village Maiden Demo (PlayStation 5)": "RE8_M_PS5_Demo.list",
    "Resident Evil 8: Village Z Version (PC Steam)": "RE8Z_PC_Release.list",
    "Resident Evil: Re:Verse (Open Beta) (PC Steam)": "RERE_PC_Open_Beta.list",
    "Resident Evil: Re:Verse (PC Steam)": "RERE_PC_Release.list",
    "Resident Evil: Re:Verse (PlayStation 4)": "RERE_PS4_Release.list",
    "Resident Evil: Resistance (Open Beta) (PC Steam)": "RER_PC_Open_Beta.list",
    "Resident Evil: Resistance (PC Steam)": "RER_PC_Release.list",
    "Street Fighter 6 (Closed Beta) (PC Steam)": "SF6_PC_Closed_Beta.list",
    "Street Fighter 6 (Open Beta) (PC Steam)": "SF6_PC_Closed_Beta.list",
    "Street Fighter 6 (PC Steam)": "SF6_PC_Release.list",
    "Street Fighter 6 (PlayStation 4)": "SF6_PS4_Release.list",
    "Street Fighter 6 Demo (PC Steam)": "SF6_PC_Demo.list",
}
