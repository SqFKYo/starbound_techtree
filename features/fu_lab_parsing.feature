Feature: Centrifuge, extraction lab and xeno lab recipes are parsed correctly

  @recipe_parsing @centrifuge @todo
  Scenario: Centrifuge recipes are read correctly
    Given Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And centrifuge recipes are parsed
    Then centrifuge extracting milk produces cheese at common
    And centrifuge extracting magmacomb produces corefragmentore at normal and liquidlava at common and scorchedcore at rare
    And centrifuge extracting ff_mercury produces ironore at common and liquidwastewater at common and fu_carbon at uncommon
    And centrifuge extracting toxicwaste produces uraniumore at common and tritium at rarest
    And centrifuge extracting sand2 produces biospore at rarest and sand at common and ff_silicon at rare

  @recipe_parsing @extraction_lab @todo
  Scenario: Extraction lab recipes are read correctly
    Given Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And extraction recipes are parsed
    Then lab extracting tentacleplant produces geneticmaterial
    And lab extracting poop produces fu_nitrogen
    And lab extracting ironblock produces ironbar
    And lab extracting choppedonion produces tissueculture

  @recipe_parsing @xeno_lab @todo
  Scenario: Xeno lab recipes are read correctly
    Given Frackin' Universe folder is C:\Games\Steam\steamapps\common\Starbound\Unpacked_FU
    When SbParser is initialized
    And xeno recipes are parsed
    Then xeno extracting soakedwheat produces wheatsprout
    And xeno extracting nakatibark produces gene_defense
    And xeno ignuschiliseed nakatibark produces gene_reactive and gene_pyro
    And xeno extracting wildvines produces gene_chloroplast
