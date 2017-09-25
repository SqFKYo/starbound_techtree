Feature: Binding human readable names to in game code names works

  @friendly_names @todo
  Scenario: Searching human readable names based on the code names
    Given vanilla Starbound folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets
    And Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And friendly names are read
    Then unfriendly name apextier1chest corresponds to friendly name Defector's Chestguard
    # Enter steps here

  @friendly_names @todo
  Scenario: Searching code names based on human readable names
    Given vanilla Starbound folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets
    And Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And friendly names are read
