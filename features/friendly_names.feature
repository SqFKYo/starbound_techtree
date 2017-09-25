Feature: Binding human readable names to in game code names works

  @friendly_names
  Scenario: Searching human readable names based on the code names
    Given vanilla Starbound folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets
    And Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And friendly names are read
    Then unfriendly name apextier1chest corresponds to friendly name Defector's Chestguard
    And unfriendly name avalihologram1 corresponds to friendly name Hologram, Planet
    And unfriendly name avaliribbon1 corresponds to friendly name Avali Ribbon, Trim Style
    And unfriendly name swtjc_wp_advancedand_nolatch corresponds to friendly name Advanced AND Gate (2 Inputs, No Latch)

  @friendly_names
  Scenario: Searching code names based on human readable names
    Given vanilla Starbound folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets
    And Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And friendly names are read
    Then friendly name Defector's Chestguard corresponds to unfriendly name apextier1chest
    And friendly name Hologram, Planet corresponds to unfriendly name avalihologram1
    And friendly name Avali Ribbon, Trim Style corresponds to unfriendly name avaliribbon1
    And friendly name Advanced AND Gate (2 Inputs, No Latch) corresponds to unfriendly name swtjc_wp_advancedand_nolatch
