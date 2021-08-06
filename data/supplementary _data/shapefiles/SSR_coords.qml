<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" minScale="0" maxScale="0" version="3.16.3-Hannover" simplifyLocal="1" readOnly="0" labelsEnabled="0" simplifyDrawingHints="0" hasScaleBasedVisibilityFlag="0" simplifyMaxScale="1" simplifyAlgorithm="0" simplifyDrawingTol="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal durationUnit="min" startField="" mode="0" fixedDuration="0" enabled="0" durationField="" endField="" endExpression="" startExpression="" accumulate="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" forceraster="0" toleranceUnit="MM" toleranceUnitScale="3x:0,0,0,0,0,0" tolerance="6" type="pointCluster">
    <renderer-v2 enableorderby="0" forceraster="0" symbollevels="0" type="singleSymbol">
      <symbols>
        <symbol force_rhr="0" name="0" alpha="1" clip_to_extent="1" type="marker">
          <layer class="SimpleMarker" locked="0" enabled="1" pass="0">
            <prop v="0" k="angle"/>
            <prop v="239,138,98,255" k="color"/>
            <prop v="1" k="horizontal_anchor_point"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="circle" k="name"/>
            <prop v="0,0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="186,94,58,0" k="outline_color"/>
            <prop v="solid" k="outline_style"/>
            <prop v="0.2" k="outline_width"/>
            <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
            <prop v="MM" k="outline_width_unit"/>
            <prop v="diameter" k="scale_method"/>
            <prop v="2.6" k="size"/>
            <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
            <prop v="MM" k="size_unit"/>
            <prop v="1" k="vertical_anchor_point"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </symbols>
      <rotation/>
      <sizescale/>
    </renderer-v2>
    <symbol force_rhr="0" name="centerSymbol" alpha="1" clip_to_extent="1" type="marker">
      <layer class="SimpleMarker" locked="0" enabled="1" pass="0">
        <prop v="0" k="angle"/>
        <prop v="239,138,98,255" k="color"/>
        <prop v="1" k="horizontal_anchor_point"/>
        <prop v="bevel" k="joinstyle"/>
        <prop v="circle" k="name"/>
        <prop v="0,0" k="offset"/>
        <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
        <prop v="MM" k="offset_unit"/>
        <prop v="35,35,35,0" k="outline_color"/>
        <prop v="solid" k="outline_style"/>
        <prop v="0" k="outline_width"/>
        <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
        <prop v="MM" k="outline_width_unit"/>
        <prop v="diameter" k="scale_method"/>
        <prop v="4" k="size"/>
        <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
        <prop v="MM" k="size_unit"/>
        <prop v="1" k="vertical_anchor_point"/>
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties" type="Map">
              <Option name="size" type="Map">
                <Option name="active" value="true" type="bool"/>
                <Option name="expression" value="@cluster_size  * 4" type="QString"/>
                <Option name="transformer" type="Map">
                  <Option name="d" type="Map">
                    <Option name="exponent" value="0.57" type="double"/>
                    <Option name="maxSize" value="10" type="double"/>
                    <Option name="maxValue" value="200" type="double"/>
                    <Option name="minSize" value="1" type="double"/>
                    <Option name="minValue" value="0" type="double"/>
                    <Option name="nullSize" value="0" type="double"/>
                    <Option name="scaleType" value="2" type="int"/>
                  </Option>
                  <Option name="t" value="1" type="int"/>
                </Option>
                <Option name="type" value="3" type="int"/>
              </Option>
            </Option>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
      </layer>
      <layer class="FontMarker" locked="0" enabled="1" pass="0">
        <prop v="0" k="angle"/>
        <prop v="A" k="chr"/>
        <prop v="255,255,255,255" k="color"/>
        <prop v="MS Shell Dlg 2" k="font"/>
        <prop v="" k="font_style"/>
        <prop v="1" k="horizontal_anchor_point"/>
        <prop v="miter" k="joinstyle"/>
        <prop v="0,-0.40000000000000002" k="offset"/>
        <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
        <prop v="MM" k="offset_unit"/>
        <prop v="255,255,255,255" k="outline_color"/>
        <prop v="0" k="outline_width"/>
        <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
        <prop v="MM" k="outline_width_unit"/>
        <prop v="2.4" k="size"/>
        <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
        <prop v="MM" k="size_unit"/>
        <prop v="1" k="vertical_anchor_point"/>
        <data_defined_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString"/>
            <Option name="properties" type="Map">
              <Option name="char" type="Map">
                <Option name="active" value="true" type="bool"/>
                <Option name="expression" value="@cluster_size" type="QString"/>
                <Option name="type" value="3" type="int"/>
              </Option>
              <Option name="offset" type="Map">
                <Option name="active" value="true" type="bool"/>
                <Option name="expression" value="'0'|| ',' || tostring(-0.1*(coalesce(scale_exp(@cluster_size  * 4, 0, 200, 1, 10, 0.57), 0)))" type="QString"/>
                <Option name="type" value="3" type="int"/>
              </Option>
              <Option name="size" type="Map">
                <Option name="active" value="true" type="bool"/>
                <Option name="expression" value="0.6*(coalesce(scale_exp(@cluster_size  * 4, 0, 200, 1, 10, 0.57), 0))" type="QString"/>
                <Option name="type" value="3" type="int"/>
              </Option>
            </Option>
            <Option name="type" value="collection" type="QString"/>
          </Option>
        </data_defined_properties>
      </layer>
    </symbol>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory maxScaleDenominator="1e+08" sizeScale="3x:0,0,0,0,0,0" lineSizeType="MM" penColor="#000000" scaleBasedVisibility="0" enabled="0" direction="1" width="15" spacingUnitScale="3x:0,0,0,0,0,0" spacing="0" scaleDependency="Area" showAxis="0" lineSizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" backgroundAlpha="255" opacity="1" penWidth="0" labelPlacementMethod="XHeight" barWidth="5" minimumSize="0" minScaleDenominator="1000" height="15" backgroundColor="#ffffff" penAlpha="255" spacingUnit="MM" sizeType="MM" rotationOffset="270">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" color="#000000" label=""/>
      <axisSymbol>
        <symbol force_rhr="0" name="" alpha="1" clip_to_extent="1" type="line">
          <layer class="SimpleLine" locked="0" enabled="1" pass="0">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString"/>
                <Option name="properties"/>
                <Option name="type" value="collection" type="QString"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="0" dist="0" showAll="1" linePlacementFlags="2" zIndex="0" priority="0" obstacle="0">
    <properties>
      <Option type="Map">
        <Option name="name" value="" type="QString"/>
        <Option name="properties"/>
        <Option name="type" value="collection" type="QString"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="ssr_station" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ssr_lat" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ssr_long" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="ssr_station" name=""/>
    <alias index="1" field="ssr_lat" name=""/>
    <alias index="2" field="ssr_long" name=""/>
  </aliases>
  <defaults>
    <default field="ssr_station" applyOnUpdate="0" expression=""/>
    <default field="ssr_lat" applyOnUpdate="0" expression=""/>
    <default field="ssr_long" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="ssr_station" exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint field="ssr_lat" exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint field="ssr_long" exp_strength="0" constraints="0" unique_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="ssr_station" exp="" desc=""/>
    <constraint field="ssr_lat" exp="" desc=""/>
    <constraint field="ssr_long" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{246060ce-53a7-43cf-83f1-8dfd133e6e4e}" key="Canvas"/>
    <actionsetting icon="" name="" isEnabledOnlyWhenEditable="0" id="{8a9e8df6-2da7-414a-9919-3dc1bfd47700}" capture="0" action="" notificationMessage="" type="0" shortTitle="">
      <actionScope id="Canvas"/>
      <actionScope id="Field"/>
      <actionScope id="Feature"/>
    </actionsetting>
  </attributeactions>
  <attributetableconfig sortExpression="" actionWidgetStyle="dropDown" sortOrder="0">
    <columns>
      <column width="-1" hidden="1" type="actions"/>
      <column name="ssr_station" width="-1" hidden="0" type="field"/>
      <column name="ssr_lat" width="-1" hidden="0" type="field"/>
      <column name="ssr_long" width="-1" hidden="0" type="field"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">C:/Users/hanna/OneDrive/Documents/Uni Assignments/Winter 2020/SSR-lakes/qGIS map/trend test</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>C:/Users/hanna/OneDrive/Documents/Uni Assignments/Winter 2020/SSR-lakes/qGIS map/trend test</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="Altitude (" editable="1"/>
    <field name="Comments" editable="1"/>
    <field name="Country" editable="1"/>
    <field name="Data acces" editable="1"/>
    <field name="Data_sourc" editable="1"/>
    <field name="ID" editable="1"/>
    <field name="ID Type" editable="1"/>
    <field name="ID2" editable="1"/>
    <field name="ID2 Type" editable="1"/>
    <field name="Instrument" editable="1"/>
    <field name="Intercept" editable="1"/>
    <field name="Lake" editable="1"/>
    <field name="Lake_formatted" editable="1"/>
    <field name="Latitude" editable="1"/>
    <field name="Longitude" editable="1"/>
    <field name="MKEndYear" editable="1"/>
    <field name="MKLength" editable="1"/>
    <field name="MKResoluti" editable="1"/>
    <field name="MKStartYea" editable="1"/>
    <field name="P" editable="1"/>
    <field name="Parameters" editable="1"/>
    <field name="Province_S" editable="1"/>
    <field name="Record end" editable="1"/>
    <field name="Record len" editable="1"/>
    <field name="Record sta" editable="1"/>
    <field name="Sample_typ" editable="1"/>
    <field name="Slope" editable="1"/>
    <field name="Source dat" editable="1"/>
    <field name="Station na" editable="1"/>
    <field name="TSI" editable="1"/>
    <field name="Temporal r" editable="1"/>
    <field name="TemporalRe" editable="1"/>
    <field name="Units" editable="1"/>
    <field name="Z" editable="1"/>
    <field name="intercept" editable="1"/>
    <field name="lake" editable="1"/>
    <field name="lat" editable="1"/>
    <field name="long" editable="1"/>
    <field name="orig_ogc_f" editable="1"/>
    <field name="p" editable="1"/>
    <field name="proportion" editable="1"/>
    <field name="record_end" editable="1"/>
    <field name="record_len" editable="1"/>
    <field name="record_sta" editable="1"/>
    <field name="slope" editable="1"/>
    <field name="ssr_lat" editable="1"/>
    <field name="ssr_long" editable="1"/>
    <field name="ssr_station" editable="1"/>
    <field name="trend" editable="1"/>
    <field name="trophic_st" editable="1"/>
    <field name="z" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="Altitude (" labelOnTop="0"/>
    <field name="Comments" labelOnTop="0"/>
    <field name="Country" labelOnTop="0"/>
    <field name="Data acces" labelOnTop="0"/>
    <field name="Data_sourc" labelOnTop="0"/>
    <field name="ID" labelOnTop="0"/>
    <field name="ID Type" labelOnTop="0"/>
    <field name="ID2" labelOnTop="0"/>
    <field name="ID2 Type" labelOnTop="0"/>
    <field name="Instrument" labelOnTop="0"/>
    <field name="Intercept" labelOnTop="0"/>
    <field name="Lake" labelOnTop="0"/>
    <field name="Lake_formatted" labelOnTop="0"/>
    <field name="Latitude" labelOnTop="0"/>
    <field name="Longitude" labelOnTop="0"/>
    <field name="MKEndYear" labelOnTop="0"/>
    <field name="MKLength" labelOnTop="0"/>
    <field name="MKResoluti" labelOnTop="0"/>
    <field name="MKStartYea" labelOnTop="0"/>
    <field name="P" labelOnTop="0"/>
    <field name="Parameters" labelOnTop="0"/>
    <field name="Province_S" labelOnTop="0"/>
    <field name="Record end" labelOnTop="0"/>
    <field name="Record len" labelOnTop="0"/>
    <field name="Record sta" labelOnTop="0"/>
    <field name="Sample_typ" labelOnTop="0"/>
    <field name="Slope" labelOnTop="0"/>
    <field name="Source dat" labelOnTop="0"/>
    <field name="Station na" labelOnTop="0"/>
    <field name="TSI" labelOnTop="0"/>
    <field name="Temporal r" labelOnTop="0"/>
    <field name="TemporalRe" labelOnTop="0"/>
    <field name="Units" labelOnTop="0"/>
    <field name="Z" labelOnTop="0"/>
    <field name="intercept" labelOnTop="0"/>
    <field name="lake" labelOnTop="0"/>
    <field name="lat" labelOnTop="0"/>
    <field name="long" labelOnTop="0"/>
    <field name="orig_ogc_f" labelOnTop="0"/>
    <field name="p" labelOnTop="0"/>
    <field name="proportion" labelOnTop="0"/>
    <field name="record_end" labelOnTop="0"/>
    <field name="record_len" labelOnTop="0"/>
    <field name="record_sta" labelOnTop="0"/>
    <field name="slope" labelOnTop="0"/>
    <field name="ssr_lat" labelOnTop="0"/>
    <field name="ssr_long" labelOnTop="0"/>
    <field name="ssr_station" labelOnTop="0"/>
    <field name="trend" labelOnTop="0"/>
    <field name="trophic_st" labelOnTop="0"/>
    <field name="z" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"Station name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
