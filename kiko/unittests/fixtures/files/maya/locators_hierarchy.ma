//Maya ASCII 2017ff05 scene
//Name: locators_hierarchy.ma
//Last modified: Fri, Sep 07, 2018 08:29:23 AM
//Codeset: 1252
requires maya "2017ff05";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201710312130-1018716";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "84A6124E-4FC1-6F65-F311-64872B27EDA9";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 34.797684663249484 16.763767186966358 30.299987774422959 ;
	setAttr ".r" -type "double3" -32.738352729602653 56.599999999999703 -2.8888882479089153e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "294F97F4-4A08-855A-E12A-45B7A1B67A3B";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 36.29086034905577;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 9.3131023592536835 -2.8624567839221351 13.496001868988042 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "F17D67D6-447C-62BC-11D6-96AB7070FB87";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "4924E070-4489-2F76-7475-A68A39205CC4";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "B20219A3-425D-28C2-956E-E1BAA66BC74D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "E5BB9DE2-4139-0611-F6B6-EA899503D224";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "B387D7F5-45F3-0AFA-9EF5-66836DE50360";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "0ADF714C-42A6-85DA-A25D-B7BD507096F1";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "parent";
	rename -uid "8B23C90F-454D-E274-A376-AF96BDE647B3";
createNode locator -n "parentShape" -p "parent";
	rename -uid "C98C7358-4027-966A-2749-7FB5C06A958C";
	setAttr -k off ".v";
createNode transform -n "childA" -p "parent";
	rename -uid "D36AC774-40FA-96CE-6C0C-8FA83B719BA6";
createNode locator -n "childAShape" -p "|parent|childA";
	rename -uid "D9C31F3F-4DC6-A7B7-3ADC-FCBBFBEF10A3";
	setAttr -k off ".v";
createNode transform -n "childB" -p "parent";
	rename -uid "547308BF-4CA6-AB0A-54CB-5A8A07E1AD01";
createNode locator -n "childBShape" -p "childB";
	rename -uid "04B0FEA4-4513-5A76-AA4D-629570433E45";
	setAttr -k off ".v";
createNode transform -n "childBA" -p "childB";
	rename -uid "70E69FA0-4349-38E3-7095-298F641836D5";
	setAttr ".t" -type "double3" 7 4 2 ;
createNode locator -n "childBAShape" -p "childBA";
	rename -uid "FAABA466-472D-BB44-A7B9-2CACF5B9E746";
	setAttr -k off ".v";
createNode transform -n "childBB" -p "childB";
	rename -uid "76941F60-4F85-6967-90A3-E4910F9CC2BC";
createNode locator -n "childBBShape" -p "childBB";
	rename -uid "11631531-4437-797F-664B-F09E2C870324";
	setAttr -k off ".v";
createNode transform -n "childBBA" -p "childBB";
	rename -uid "94D2251E-4CFD-BFE3-CB49-9781A917F52E";
	setAttr ".t" -type "double3" 5 6 9 ;
	setAttr ".r" -type "double3" 90 13.001 9.746 ;
createNode locator -n "childBBAShape" -p "childBBA";
	rename -uid "A9691F23-4251-F909-B821-B3A536EA7F79";
	setAttr -k off ".v";
createNode transform -n "childBBB" -p "childBB";
	rename -uid "4C1498DC-480B-F37A-1985-2E8E11BA7DFE";
createNode locator -n "childBBBShape" -p "childBBB";
	rename -uid "7A1012D2-4D59-AC14-09F6-6B961AAEE01D";
	setAttr -k off ".v";
createNode transform -n "childA" -p "childB";
	rename -uid "A43E7643-43A7-07C8-BE7F-B7A4D31A14D8";
	setAttr ".t" -type "double3" -13.021560828613334 10.529645055948684 5.1243270366518274 ;
	setAttr ".r" -type "double3" 23.744079208512062 -41.202358987314099 21.658295017163304 ;
	setAttr ".s" -type "double3" 2.867541326131652 1.5370979842153014 1.906897526955567 ;
createNode locator -n "childAShape" -p "|parent|childB|childA";
	rename -uid "BC746199-4547-5641-73B3-7D8F14D88C41";
	setAttr -k off ".v";
createNode transform -n "childC" -p "parent";
	rename -uid "C68F3A09-40DB-6757-309C-EF87DA077A12";
createNode locator -n "childCShape" -p "childC";
	rename -uid "464ADB06-4693-C09C-CE26-9E875191F840";
	setAttr -k off ".v";
createNode transform -n "childD" -p "parent";
	rename -uid "1D8B8B0F-4EB1-ED47-0146-BB8BADE114B0";
createNode locator -n "childDShape" -p "childD";
	rename -uid "8EB131F7-488F-F9C4-B14C-3580D15594CF";
	setAttr -k off ".v";
createNode parentConstraint -n "childD_parentConstraint1" -p "childD";
	rename -uid "EF0A7548-4145-45D5-6A09-22AEA1290369";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "childBBBW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg[0].tot" -type "double3" 8.162437392682353 -8.9217561301594301 12.696316893000848 ;
	setAttr ".tg[0].tor" -type "double3" -14.967400810939584 -52.649445735042555 -0.58951184903689824 ;
	setAttr ".lr" -type "double3" -1.7317150452230759e-014 -79.999999999999943 1.8163743914647859e-014 ;
	setAttr ".rst" -type "double3" -5.9168222286692105 -3.3234391793729627 8.4094016131989022 ;
	setAttr ".rsrr" -type "double3" -5.8866760614574382e-015 -79.999999999999943 7.01546734468024e-015 ;
	setAttr -k on ".w0";
createNode scaleConstraint -n "childD_scaleConstraint1" -p "childD";
	rename -uid "1263310D-4D8E-B7D6-5B73-9AB482F86323";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "childBBBW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "A89597C2-4946-CABA-6E72-B3AFF5D5AEB4";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "2721513D-4F8E-0294-D6C8-26B7F0BF720D";
createNode displayLayer -n "defaultLayer";
	rename -uid "552648B1-44CA-3EA7-DAA4-86B3858B46B6";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "B8A2FF52-4015-7B89-96D9-B78B1489437C";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "8C20AECC-49F2-E802-E55F-32B155952BF7";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "8CDB1D93-4A6B-15F9-C29B-E9B7AC6E261E";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n"
		+ "            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n"
		+ "            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n"
		+ "            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n"
		+ "            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1263\n            -height 615\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n"
		+ "            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n"
		+ "            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 1\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n"
		+ "            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 0\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n"
		+ "            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n"
		+ "                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n"
		+ "                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n"
		+ "                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n"
		+ "                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n"
		+ "                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n"
		+ "\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1263\\n    -height 615\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1263\\n    -height 615\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "6C6FDE06-40EE-17A0-406C-3B93280ADFE3";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode animCurveTL -n "parent_translateX";
	rename -uid "BA4D3A07-4A3F-683B-8F01-059F8D68436A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  1 0 60 16.3319127627257 120 11.748532486646013;
createNode animCurveTL -n "parent_translateY";
	rename -uid "1DA64DAD-4DA0-DE0B-2B08-5DAF4CAAA2F0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 0 25 -1.8592375750289043 60 5.7334236960810108
		 92 -1.1413744442315603 120 0;
createNode animCurveTL -n "parent_translateZ";
	rename -uid "0BAF6CDC-47E5-513A-9555-569E27E206C8";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTU -n "parent_visibility";
	rename -uid "CE338EC2-40A5-B45D-01EE-BFB72A11CF8A";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
	setAttr ".kot[0]"  5;
createNode animCurveTA -n "parent_rotateX";
	rename -uid "D62F8F88-40B4-24FF-B6DC-B6BE901E7FC7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTA -n "parent_rotateY";
	rename -uid "54682BF4-4A20-13DA-E2E5-B892345ADBEF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTA -n "parent_rotateZ";
	rename -uid "E5C4617E-4D3D-3F4A-F838-3CBCE6E4C602";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTU -n "parent_scaleX";
	rename -uid "D8564954-4956-94B6-A836-ED9270A225B0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "parent_scaleY";
	rename -uid "9D9F2287-46A4-654D-3181-0FBE85B761BC";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "parent_scaleZ";
	rename -uid "3AFCDCF9-4780-1757-FEA2-68A1C2CA6CB2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTL -n "childA_translateX";
	rename -uid "03E1881B-4BB0-3788-DFDD-6FACE75E11B0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTL -n "childA_translateY";
	rename -uid "BFC1085E-4FCF-D66A-F3D0-A098CBF17F73";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTL -n "childA_translateZ";
	rename -uid "22C6274C-4C69-F3E5-8FE6-F8A2FA8642A0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTU -n "childA_visibility";
	rename -uid "2B3B1E04-4430-05FF-B14E-A8B3F2476B1E";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
	setAttr ".kot[0]"  5;
createNode animCurveTA -n "childA_rotateX";
	rename -uid "F952D2A7-4AC4-850F-D394-6EAC80955EA6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 37 51.233379017281564 75 139.10287181219508
		 105 142.33517548981425;
createNode animCurveTA -n "childA_rotateY";
	rename -uid "1651641A-4CBC-153A-5CD5-5AB9DD42CA97";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 37 -42.430287021703734 75 10.067133448765077
		 105 -17.081800401669927;
createNode animCurveTA -n "childA_rotateZ";
	rename -uid "308DDB09-47D3-986D-350D-03823D995D19";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 37 -10.330093784593583 75 -75.325390939089303
		 105 -136.33563152102562;
createNode animCurveTU -n "childA_scaleX";
	rename -uid "C7CC0251-400A-458B-13BC-5397AB0FECA6";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "childA_scaleY";
	rename -uid "D2F3535E-47CA-9E9A-0D7C-7281C1DF185D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "childA_scaleZ";
	rename -uid "EB4C20CE-4028-F202-D226-D9A4CC6E7D10";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTA -n "childC_rotateX";
	rename -uid "39F1F85E-47C6-08E9-E59A-26941BE4EBE4";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTA -n "childC_rotateY";
	rename -uid "C5BAC312-46B4-D71D-EF06-D8B3175FAEA2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 90 1000.0000000000001;
createNode animCurveTA -n "childC_rotateZ";
	rename -uid "54283EB0-400A-F425-3792-ED849AFE692A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTU -n "childC_visibility";
	rename -uid "9E9ADEB6-42EE-36A8-AB6D-FEBAE2F46E26";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
	setAttr ".kot[0]"  5;
createNode animCurveTL -n "childC_translateX";
	rename -uid "20A19D6F-4977-45BA-123B-298272357D95";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 40 -9.1968710245729355 67 -9.8403053826174336
		 90 -5.9168222286692114;
createNode animCurveTL -n "childC_translateY";
	rename -uid "B871D08B-44FE-D04E-E471-08A9E9EE6C56";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 40 0.3126300788323455 67 1.1102113235892475
		 90 -3.3234391793729614;
createNode animCurveTL -n "childC_translateZ";
	rename -uid "5A262193-49D8-C8E4-E304-4C8906BF4B40";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 0 40 8.9623984654486577 67 9.0076468899254571
		 90 8.4094016131989093;
createNode animCurveTU -n "childC_scaleX";
	rename -uid "F80ABE16-49DA-CD56-002F-28AD74542A2A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "childC_scaleY";
	rename -uid "73FEC73B-4CAC-A5A1-B00E-65855FDEB419";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "childC_scaleZ";
	rename -uid "C578375B-4777-202E-3F70-198B4C7F2A4B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTL -n "childBB_translateX";
	rename -uid "26D27740-47D7-774F-AFC3-29BB843F37BB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 120 ".ktv[0:119]"  1 -5.678496329935605 2 -5.7141746387330814
		 3 -5.8102801443737118 4 -5.9504187643533122 5 -6.1181963040939635 6 -6.2972187691682642
		 7 -6.4710919249154273 8 -6.6234218299387866 9 -6.7378141548289863 10 -6.8279620505604584
		 11 -6.9175615936120565 12 -7.005223024092647 13 -7.0895568343596684 14 -7.1691732171269011
		 15 -7.2426827679638706 16 -7.3086957354013578 17 -7.3658224108659009 18 -7.4126733255833956
		 19 -7.4478587572746093 20 -7.4699890504106818 21 -7.4776746360919617 22 -7.4586348250585273
		 23 -7.4058300755333413 24 -7.3257321091845551 25 -7.2248130155739672 26 -7.1095442066428571
		 27 -6.9863982100782342 28 -6.8618465662196666 29 -6.7423607993203429 30 -6.6344134611968499
		 31 -6.5444760523497383 32 -6.4790202793871821 33 -6.4445183849642547 34 -6.4285753430891219
		 35 -6.4144025089131276 36 -6.4018811027589653 37 -6.3908922211108541 38 -6.3813169779913936
		 39 -6.373036567415701 40 -6.3659320995318787 41 -6.3598846979456471 42 -6.3547755364856915
		 43 -6.3504857359034252 44 -6.3468964263271186 45 -6.3438887675201672 46 -6.3413438877767252
		 47 -6.3391429206870376 48 -6.3371670180703585 49 -6.3352973073922945 50 -6.3334149440936098
		 51 -6.3314010456874961 52 -6.3291367612838121 53 -6.3265032457232833 54 -6.3233816079228085
		 55 -6.3196530002702014 56 -6.3151985890456661 57 -6.3109150951279629 58 -6.3076439703000347
		 59 -6.3051833509897541 60 -6.3033313342819097 61 -6.3018860606644793 62 -6.3006456613158619
		 63 -6.299408247285208 64 -6.2979719503456071 65 -6.2961349068222034 66 -6.2936952209360708
		 67 -6.2904510261416302 68 -6.2862004743069919 69 -6.2807416420327113 70 -6.2738726748507627
		 71 -6.2653917505684387 72 -6.2550968973733418 73 -6.2288592344202272 74 -6.1759612659899537
		 75 -6.1013170764501714 76 -6.009841610071228 77 -5.9064501963595388 78 -5.7960563418289262
		 79 -5.683575321859812 80 -5.5739224596038834 81 -5.4720111899180983 82 -5.3827568661944705
		 83 -5.3110745521314779 84 -5.2618781171261766 85 -5.2400827394836931 86 -5.2339782204269651
		 87 -5.2285512116184867 88 -5.2237618942072901 89 -5.2195704347468581 90 -5.2159369296636742
		 91 -5.2128215488180318 92 -5.2101844502113384 93 -5.2079857480583955 94 -5.2061856029832514
		 95 -5.2047441664877407 96 -5.2036215664699821 97 -5.2027779604752764 98 -5.2021734803927089
		 99 -5.2017682845657669 100 -5.2015225096727029 101 -5.20139629968953 102 -5.2013498020130831
		 103 -5.2013431594791051 104 -5.2013431594791051 105 -5.2013431594791051 106 -5.2013431594791051
		 107 -5.2013431594791051 108 -5.2013431594791051 109 -5.2013431594791051 110 -5.2013431594791051
		 111 -5.2013431594791051 112 -5.2013431594791051 113 -5.2013431594791051 114 -5.2013431594791051
		 115 -5.2013431594791051 116 -5.2013431594791051 117 -5.2013431594791051 118 -5.2013431594791051
		 119 -5.2013431594791051 120 -5.2013431594791051;
createNode animCurveTL -n "childBB_translateY";
	rename -uid "9CFB9D2B-49B7-93D7-746E-699A692935F7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 120 ".ktv[0:119]"  1 0.054378305202241961 2 0.020906201328387337
		 3 -0.067338425917951694 4 -0.19209809404735051 5 -0.33511522262946775 6 -0.47813240263056611
		 7 -0.60289202913507423 8 -0.69113670290334828 9 -0.72460878963754394 10 -0.6229930397598068
		 11 -0.34205511577515008 12 0.082340185798783105 13 0.61432904322861126 14 1.2180458519518262
		 15 1.8576279317587028 16 2.4972100115655795 17 3.1009268202887936 18 3.6329156777186222
		 19 4.0573112358147148 20 4.3382487621900037 21 4.4398646531549497 22 4.4233724342134844
		 23 4.376558057972753 24 4.3034146764819026 25 4.20793577737542 26 4.0941141994338999
		 27 3.9659438770784501 28 3.8274177826076663 29 3.6825287698075404 30 3.5352709508681284
		 31 3.3896371920662487 32 3.249620378264642 33 3.1192145937744726 34 2.9888377575386444
		 35 2.8472974121876025 36 2.6961720938473954 37 2.5370391352508914 38 2.3714757774906357
		 39 2.2010606941531941 40 2.0273711424703125 41 1.8519843422003595 42 1.6764790231399811
		 43 1.5024324076450204 44 1.3314217347648851 45 1.1650257092558682 46 1.0048215592231262
		 47 0.85238658363232522 48 0.70929938094896805 49 0.5771368646665298 50 0.45747784020930116
		 51 0.35189866666739311 52 0.26197780202073728 53 0.18929334586021351 54 0.13542219485925466
		 55 0.10194255174789779 56 0.090432152533160171 57 0.10029663921465824 58 0.12890183088041735
		 59 0.17476501598122349 60 0.23640432388210128 61 0.31233713754529152 62 0.40108051278174295
		 63 0.50115306968318429 64 0.61107193312498942 65 0.72935400261921268 66 0.8545182363024012
		 67 0.98508157730400492 68 1.1195608451781269 69 1.2564751834242462 70 1.3943414297668324
		 71 1.5316764001429799 72 1.6669992707332142 73 1.811032228547548 74 1.9731955616978978
		 75 2.1500561833425489 76 2.3381782551302677 77 2.5341256809565422 78 2.7344657606093903
		 79 2.9357624329403347 80 3.1345796149063014 81 3.3274846391371873 82 3.5110413985811979
		 83 3.6818140001506254 84 3.8363694555293897 85 3.9712717886563063 86 4.0955238110440995
		 87 4.2198413001835604 88 4.3433548183384252 89 4.4651949461738045 90 4.584494353587024
		 91 4.7003836091865159 92 4.8119933596326314 93 4.9184561577448722 94 5.0189026232142515
		 95 5.1124635134342524 96 5.1982711746707748 97 5.2754559071051599 98 5.3431502281278309
		 99 5.4004838663784041 100 5.4465889388294473 101 5.480597048447148 102 5.5016386948814313
		 103 5.5088456245122828 104 5.5088456245122828 105 5.5088456245122828 106 5.5088456245122828
		 107 5.5088456245122828 108 5.5088456245122828 109 5.5088456245122828 110 5.5088456245122828
		 111 5.5088456245122828 112 5.5088456245122828 113 5.5088456245122828 114 5.5088456245122828
		 115 5.5088456245122828 116 5.5088456245122828 117 5.5088456245122828 118 5.5088456245122828
		 119 5.5088456245122828 120 5.5088456245122828;
createNode animCurveTL -n "childBB_translateZ";
	rename -uid "99DA1863-4580-95AB-2D02-37BAA0D6A475";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 120 ".ktv[0:119]"  1 5.6377126010339467 2 5.7092142867865139
		 3 5.8977187091705714 4 6.1642250100234062 5 6.4697321219650785 6 6.7752393437457945
		 7 7.0417455556813069 8 7.2302500774435448 9 7.3017517265831007 10 7.2405092187814759
		 11 7.0710869587395297 12 6.8149433287803918 13 6.4935361229144144 14 6.1283242126509387
		 15 5.740764700746098 16 5.3523162566411902 17 4.984437554864023 18 4.6585856905409679
		 19 4.3962193829724061 20 4.2187969881917464 21 4.1477761462257519 22 4.1379732045055642
		 23 4.1297999822866958 24 4.1231083009363161 25 4.1177500246330183 26 4.1135769776051294
		 27 4.1104410285879043 28 4.1081940092274936 29 4.1066877613430552 30 4.1057741384103279
		 31 4.1053049803410335 32 4.1051321321333987 33 4.1051074396334002 34 4.1169042379499103
		 35 4.1508861881731827 36 4.2049402333145673 37 4.2769535823632605 38 4.3648136498367265
		 39 4.4664070704538421 40 4.5796212164174595 41 4.7023435929192985 42 4.8324606351948853
		 43 4.9678598242561662 44 5.1064287015645586 45 5.2460536116813579 46 5.3846220900230435
		 47 5.5200216599161696 48 5.6501386840569214 49 5.7728610363789068 50 5.8860748438253676
		 51 5.987668536465236 52 6.07552856162396 53 6.1475416809646415 54 6.2015958530499606
		 55 6.2355777428236037 56 6.2473744746458095 57 6.2414733891085188 58 6.2240494522206538
		 59 6.1955218377744012 60 6.1563091968840418 61 6.1068306410037225 62 6.0475055165549509
		 63 5.9787521222011319 64 5.9009897492179659 65 5.8146378950796223 66 5.7201145491519512
		 67 5.6178391609555467 68 5.5082313574405788 69 5.391708861828663 70 5.2686912603086276
		 71 5.1395982877299833 72 5.0048474443234312 73 4.8505534729225461 74 4.6662836548031015
		 75 4.4576330723723459 76 4.230199917513394 77 3.9895828120068968 78 3.7413761934141103
		 79 3.49117862408227 80 3.2445887119277055 81 3.0072008261580661 82 2.7846136113385143
		 83 2.582425373274869 84 2.4062309893135536 85 2.2616288979914678 86 2.1377744917392394
		 87 2.0201574390737829 88 1.9088802377637919 89 1.8040452404707628 90 1.7057530183757532
		 91 1.6141059612906188 92 1.5292063069319657 93 1.4511548546236166 94 1.3800538809795522
		 95 1.3160055035304525 96 1.2591107602249774 97 1.2094720723210692 98 1.1671904219823594
		 99 1.1323685475874392 100 1.1051076926360444 101 1.085509446746225 102 1.0736760291186063
		 103 1.0697089410949019 104 1.0697089410949019 105 1.0697089410949019 106 1.0697089410949019
		 107 1.0697089410949019 108 1.0697089410949019 109 1.0697089410949019 110 1.0697089410949019
		 111 1.0697089410949019 112 1.0697089410949019 113 1.0697089410949019 114 1.0697089410949019
		 115 1.0697089410949019 116 1.0697089410949019 117 1.0697089410949019 118 1.0697089410949019
		 119 1.0697089410949019 120 1.0697089410949019;
createNode animCurveTU -n "childBB_visibility";
	rename -uid "6AA0D8A4-46E7-3190-5996-7BAC7F2EF9FF";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
	setAttr ".kot[0]"  5;
createNode animCurveTA -n "childBB_rotateX";
	rename -uid "A1D06069-4EC0-F190-3A14-C598DB56F53C";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTA -n "childBB_rotateY";
	rename -uid "05107B3D-4BBC-1BD2-A80D-42B9042A2D65";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTA -n "childBB_rotateZ";
	rename -uid "FE388D6F-4AFD-7B09-10B8-01B872346214";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 0;
createNode animCurveTU -n "childBB_scaleX";
	rename -uid "96B7C55B-490E-F67E-DB54-F78B7AA89AD7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "childBB_scaleY";
	rename -uid "73DCA8B4-43E2-9F8F-3C25-C59C4B0A2EA5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTU -n "childBB_scaleZ";
	rename -uid "269CC571-4CCD-E1CA-B518-E6843122281A";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  1 1;
createNode animCurveTL -n "childBBB_translateX";
	rename -uid "B5C19D99-46EA-36D1-548D-4C917445226F";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 -4.499360058404168;
createNode animCurveTL -n "childBBB_translateY";
	rename -uid "E7EA7CA7-4E77-33FB-7F95-08988F71D403";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 -4.4408920985006262e-016;
createNode animCurveTL -n "childBBB_translateZ";
	rename -uid "1E54B9E7-4ABE-6F14-9575-FBB73288B39D";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 -7.3263418664315365;
createNode animCurveTU -n "childBBB_visibility";
	rename -uid "C9E93538-4E7B-4096-3694-0FB69D0EDCD5";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 1;
	setAttr ".kot[0]"  5;
createNode animCurveTA -n "childBBB_rotateX";
	rename -uid "36C3135A-4D44-B620-EDDD-4FB56251D2AE";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 2.5934906431567;
createNode animCurveTA -n "childBBB_rotateY";
	rename -uid "7C91A809-4603-8825-35D8-CDA0A4AF888B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 -27.681334383992386;
createNode animCurveTA -n "childBBB_rotateZ";
	rename -uid "0E502376-4744-0F40-F334-4AAC4FFDAA2B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 14.066984123279383;
createNode animCurveTU -n "childBBB_scaleX";
	rename -uid "57046BE5-469B-CEB0-96A6-39A4F5EAB6D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 1;
createNode animCurveTU -n "childBBB_scaleY";
	rename -uid "742F0AA4-49E4-F809-FF03-13BA11293170";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 1;
createNode animCurveTU -n "childBBB_scaleZ";
	rename -uid "5B6B490C-4838-C1DB-94A3-4D94F556141B";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr ".ktv[0]"  28 1;
createNode animCurveTA -n "childBA_rotateX";
	rename -uid "8D2D8E67-422D-CFB9-FE26-7DB395BF6588";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  1 33.444506369735045 32 -30.335331494916637
		 65 9.1116946702653472 88 -21.245643341323472 112 11.776183672338762;
	setAttr -s 5 ".kot[1:4]"  17 5 18 18;
createNode animCurveTA -n "childBA_rotateZ";
	rename -uid "CD1C0A79-4FA1-4F7A-643C-B2BE827BCDA6";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  1 93.061343084955922 32 62.023887975901296
		 65 112.18945013053114 88 126.72790299174746 112 50.78535115013657;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kwl[0:4]" yes no yes yes yes;
	setAttr -s 5 ".kix[1:4]"  0.83072280883789063 1.3749998807907104 
		0.95833349227905273 0.9999997615814209;
	setAttr -s 5 ".kiy[1:4]"  0.50189417600631714 0.12166228145360947 
		-0.51798141002655029 0;
	setAttr -s 5 ".kox[1:4]"  2.6335411071777344 0.95833349227905273 
		0.9999997615814209 0.9999997615814209;
	setAttr -s 5 ".koy[1:4]"  1.2187067270278931 0.53632330894470215 
		0.31864640116691589 0;
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "9D8146BC-4E4D-B65D-8F39-4987D0E72596";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "2A75FC2F-4726-80DA-DF5A-1A849FE684E5";
select -ne :time1;
	setAttr ".o" 17;
	setAttr ".unw" 17;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "parent_translateX.o" "parent.tx";
connectAttr "parent_translateY.o" "parent.ty";
connectAttr "parent_translateZ.o" "parent.tz";
connectAttr "parent_visibility.o" "parent.v";
connectAttr "parent_rotateX.o" "parent.rx";
connectAttr "parent_rotateY.o" "parent.ry";
connectAttr "parent_rotateZ.o" "parent.rz";
connectAttr "parent_scaleX.o" "parent.sx";
connectAttr "parent_scaleY.o" "parent.sy";
connectAttr "parent_scaleZ.o" "parent.sz";
connectAttr "childA_translateX.o" "|parent|childA.tx";
connectAttr "childA_translateY.o" "|parent|childA.ty";
connectAttr "childA_translateZ.o" "|parent|childA.tz";
connectAttr "childA_visibility.o" "|parent|childA.v";
connectAttr "childA_rotateX.o" "|parent|childA.rx";
connectAttr "childA_rotateY.o" "|parent|childA.ry";
connectAttr "childA_rotateZ.o" "|parent|childA.rz";
connectAttr "childA_scaleX.o" "|parent|childA.sx";
connectAttr "childA_scaleY.o" "|parent|childA.sy";
connectAttr "childA_scaleZ.o" "|parent|childA.sz";
connectAttr "childBA_rotateX.o" "childBA.rx";
connectAttr "childBA_rotateZ.o" "childBA.rz";
connectAttr "childBB_translateX.o" "childBB.tx";
connectAttr "childBB_translateY.o" "childBB.ty";
connectAttr "childBB_translateZ.o" "childBB.tz";
connectAttr "childBB_visibility.o" "childBB.v";
connectAttr "childBB_rotateX.o" "childBB.rx";
connectAttr "childBB_rotateY.o" "childBB.ry";
connectAttr "childBB_rotateZ.o" "childBB.rz";
connectAttr "childBB_scaleX.o" "childBB.sx";
connectAttr "childBB_scaleY.o" "childBB.sy";
connectAttr "childBB_scaleZ.o" "childBB.sz";
connectAttr "childBBB_visibility.o" "childBBB.v";
connectAttr "childBBB_translateX.o" "childBBB.tx";
connectAttr "childBBB_translateY.o" "childBBB.ty";
connectAttr "childBBB_translateZ.o" "childBBB.tz";
connectAttr "childBBB_rotateX.o" "childBBB.rx";
connectAttr "childBBB_rotateY.o" "childBBB.ry";
connectAttr "childBBB_rotateZ.o" "childBBB.rz";
connectAttr "childBBB_scaleX.o" "childBBB.sx";
connectAttr "childBBB_scaleY.o" "childBBB.sy";
connectAttr "childBBB_scaleZ.o" "childBBB.sz";
connectAttr "childC_translateX.o" "childC.tx";
connectAttr "childC_translateY.o" "childC.ty";
connectAttr "childC_translateZ.o" "childC.tz";
connectAttr "childC_visibility.o" "childC.v";
connectAttr "childC_rotateX.o" "childC.rx";
connectAttr "childC_rotateY.o" "childC.ry";
connectAttr "childC_rotateZ.o" "childC.rz";
connectAttr "childC_scaleX.o" "childC.sx";
connectAttr "childC_scaleY.o" "childC.sy";
connectAttr "childC_scaleZ.o" "childC.sz";
connectAttr "childD_parentConstraint1.ctx" "childD.tx";
connectAttr "childD_parentConstraint1.cty" "childD.ty";
connectAttr "childD_parentConstraint1.ctz" "childD.tz";
connectAttr "childD_parentConstraint1.crx" "childD.rx";
connectAttr "childD_parentConstraint1.cry" "childD.ry";
connectAttr "childD_parentConstraint1.crz" "childD.rz";
connectAttr "childD_scaleConstraint1.csx" "childD.sx";
connectAttr "childD_scaleConstraint1.csy" "childD.sy";
connectAttr "childD_scaleConstraint1.csz" "childD.sz";
connectAttr "childD.ro" "childD_parentConstraint1.cro";
connectAttr "childD.pim" "childD_parentConstraint1.cpim";
connectAttr "childD.rp" "childD_parentConstraint1.crp";
connectAttr "childD.rpt" "childD_parentConstraint1.crt";
connectAttr "childBBB.t" "childD_parentConstraint1.tg[0].tt";
connectAttr "childBBB.rp" "childD_parentConstraint1.tg[0].trp";
connectAttr "childBBB.rpt" "childD_parentConstraint1.tg[0].trt";
connectAttr "childBBB.r" "childD_parentConstraint1.tg[0].tr";
connectAttr "childBBB.ro" "childD_parentConstraint1.tg[0].tro";
connectAttr "childBBB.s" "childD_parentConstraint1.tg[0].ts";
connectAttr "childBBB.pm" "childD_parentConstraint1.tg[0].tpm";
connectAttr "childD_parentConstraint1.w0" "childD_parentConstraint1.tg[0].tw";
connectAttr "childD.pim" "childD_scaleConstraint1.cpim";
connectAttr "childBBB.s" "childD_scaleConstraint1.tg[0].ts";
connectAttr "childBBB.pm" "childD_scaleConstraint1.tg[0].tpm";
connectAttr "childD_scaleConstraint1.w0" "childD_scaleConstraint1.tg[0].tw";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of locators_hierarchy.ma
