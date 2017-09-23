Feature: Centrifuge, extraction lab and xeno lab recipes are parsed correctly

  @recipe_parsing @centrifuge @todo
  Scenario: Centrifuge recipes are read correctly
    Given Farckin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When centrifuge recipes are parsed

  @recipe_parsing @extraction_lab @todo
  Scenario: Centrifuge recipes are read correctly
    Given Farckin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When extraction recipes are parsed
    Then extracting tentacleplant produces geneticmaterial
    And extracting poop produces fu_nitrogen
    And extracting ironblock produces ironbar
    And extracting choppedonion produces tissueculture

  @recipe_parsing @xeno_lab @todo
  Scenario: Centrifuge recipes are read correctly
    Given Farckin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When xeno recipes are parsed