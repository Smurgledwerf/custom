The custom layouts in the database have been migrated to custom/custom_layouts so they could be integrated with GitHub.
The view tag (just within the <config> tag) had to be renamed to something unique to avoid recursion.

<config>
<client_view>
<html>
<element name="client_view_element">
  <display class="tactic.ui.panel.CustomLayoutWdg">
    <!-- WIDGET_CONFIG00939
         DO NOT EDIT THIS IN THE CUSTOM LAYOUT EDITOR!
         The code was moved to the file path below
         so that it could be integrated with GitHub.-->
    <include>/opt/spt/custom/custom_layouts/client_view_conf.xml</include>
    <view>client_view_conf</view>
  </display>
</element>
</html>
</client_view>
</config>
