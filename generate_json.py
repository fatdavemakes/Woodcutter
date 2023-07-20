import os

WORD_TO_REPLACE = "WOOD"
WORD_TO_REPLACE_LOG = "WOOD_log"
WORD_TO_REPLACE_STRIPPED_WOOD = "WOOD_wood"
WORD_TO_REPLACE_SAPLING = "WOOD_sapling"
TEMPLATES_DIR_RELATIVE = "templates"
OUTPUT_DIR_RELATIVE = os.path.join("data", "woodcutter", "recipes")
#ADVANCEMENT_DIR_RELATIVE = "\\data\\woodcutter\\advancements\\recipes\\misc"
woods = ['oak', 'spruce', 'birch', 'dark_oak', 'acacia', 'jungle', 'mangrove', 'cherry', ('mangrove', 'mangrove_log', 'mangrove_wood', 'mangrove_propagule', True), ('bamboo', 'bamboo_block', 'bamboo_block', 'bamboo', False), ('warped', 'warped_stem', 'warped_hyphae', 'warped_fungus', True), ('crimson', 'crimson_stem', 'crimson_hyphae', 'crimson_fungus', True)]
# format for each wood item is ('<plank/generic>', <optional_log_and_stripped_override>, <optional_stripped_wood_override>, <optional_sapling_override>, <has wood type>)
# if specifying any optional fields, you must specify them all, so that order is maintained

currentDir = os.path.dirname(os.path.abspath(__file__))
templatesDir = os.path.join(currentDir,TEMPLATES_DIR_RELATIVE)
outputDir = os.path.join(currentDir, OUTPUT_DIR_RELATIVE)
#advanceDir = currentDir + ADVANCEMENT_DIR_RELATIVE
print("Reading templates from " + templatesDir + "\nOutputting to " + outputDir)
templateFiles = os.listdir(templatesDir)
print("Found the following templates: ")
print(templateFiles)

if(not(os.path.exists(outputDir))):
        print("Output directory did not exist; creating")
        os.makedirs(outputDir)
#if(not(os.path.exists(advanceDir))):
#        print("Advancement directory did not exist; creating")
#        os.makedirs(advanceDir)

#eachVariantRecipeNames = []
#for variant in woods:
#        eachVariantRecipeNames["" + variant] = []

for file in templateFiles:
        if ".json" in file:
                print('\nProcessing recipe template ' + file )
                newLines = []
                with open(os.path.join(templatesDir, file), "r") as f:
                        #read_data = f.read()
                        for line in f:
                                newLines.append(line)
                                #print(line, end='')
                #print(newLines)
                for variant in woods:
                        has_overrides = type(variant) is tuple

                        primary_name = variant[0] if has_overrides else variant
                        log_and_stripped_override_name = variant[1] if has_overrides else None
                        stripped_wood_override_name = variant[2] if has_overrides else None
                        sapling_override_name = variant[3] if has_overrides else None
                        has_wood_type = variant[4] if has_overrides else True
                        
                        
                        print("\t" + primary_name + " (has overrides?: " + str(has_overrides) + ")")
                        if "_wood" in file and not has_wood_type:
                            break # We don't do wood variants if the wood type(bamboo) doesn't have one
                        if "stripped_wood" in file and not has_wood_type:
                            break # We don't do stripped wood variants if the wood type(bamboo) doesn't have one

                        newFileName = file.replace(WORD_TO_REPLACE, primary_name)
                        if "boat" in newFileName and has_overrides:
                            break # override woods don't have boat variants, so don't generate boat related recipes for them
                        with open(os.path.join(outputDir,newFileName), "w+") as newfile:
                                for line in newLines:
                                        resultLine = line
                                        if has_overrides: # first, replace the more specific lines, then the general ones
                                            resultLine = resultLine.replace(WORD_TO_REPLACE_LOG, log_and_stripped_override_name)
                                            resultLine = resultLine.replace(WORD_TO_REPLACE_STRIPPED_WOOD, stripped_wood_override_name)
                                            resultLine = resultLine.replace(WORD_TO_REPLACE_SAPLING, sapling_override_name)
                                        # regardless of overrides, replace WOOD with the wood variant
                                        resultLine = resultLine.replace(WORD_TO_REPLACE, primary_name)
                                        #print("Writing: " + resultLine)
                                        newfile.write(resultLine)
                        #print("appending " + newFileName + " to " + variant + " recipe list")
                        #eachVariantRecipeNames[variant].append(newFileName)

#for variant in woods:
#        print("Writing advancement for " + variant")

print("Generation complete, copy the contents of this folder to a datapack (ex `<save folder>/datapacks/woodcutter` and use `/datapack enable \"file/woodcutter\"` to enable")
print("Remember to delete the output directory if you're changed template file names and are re-running the script!")
