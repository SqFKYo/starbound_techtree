Feature: Recipe materials and outputs are parsed correctly

  @recipe_finding
  Scenario: Recipes are found in the data structure
    Given vanilla Starbound folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets
    And Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And crafting recipes are parsed
    Then aviantier1head recipe is found
    And pettether recipe is found
    And blastingdynamite recipe is found
    And avikancactusseed recipe is found

  @recipe_parsing
  Scenario: Recipes are parsed correctly
    Given vanilla Starbound folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_Assets
    And Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And crafting recipes are parsed
    Then aviantier1head is crafted using ironbar and fabric
    And pettether is crafted using durasteelbar and diamond and phasematter
    And blastingdynamite is crafted using ammoniumsulfate and saltpeter and ff_plastic
    And avikancactusseed is crafted using cacti and gene_immunity and gene_stimulant
