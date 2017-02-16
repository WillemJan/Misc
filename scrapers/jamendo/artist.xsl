<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" version="4.0" encoding="iso-8859-1" indent="yes"/>

<xsl:template match="/">


<xsl:text disable-output-escaping="yes">&lt;add&gt;</xsl:text>
<xsl:for-each select="//Artists/artist">
   <xsl:text disable-output-escaping="yes">&lt;doc&gt;</xsl:text>
       <xsl:apply-templates/> 
   <xsl:text disable-output-escaping="yes">&lt;/doc&gt;</xsl:text>
</xsl:for-each>
<xsl:text disable-output-escaping="yes">&lt;/add&gt;</xsl:text>
</xsl:template>

<xsl:template match="id">
   <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
   <xsl:text>id_int</xsl:text><xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
   <xsl:value-of select="."/>
   <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
</xsl:template>

<xsl:template match="name">
   <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
   <xsl:text>name_str</xsl:text><xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
   <xsl:value-of select="."/>
   <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
</xsl:template>

<xsl:template match="url">
   <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
   <xsl:text disable-output-escaping="yes">url_ignore"&gt;</xsl:text>
   <xsl:value-of select="."/>
   <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
</xsl:template>

<xsl:template match="image">
   <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
   <xsl:text disable-output-escaping="yes">image_ignore"&gt;</xsl:text>
   <xsl:value-of select="."/>
   <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
</xsl:template>

<xsl:template match="location/*">
   <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
   <xsl:value-of select="name(.)"/><xsl:text disable-output-escaping="yes">_str"&gt;</xsl:text>
   <xsl:value-of select="."/>
   <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
</xsl:template>

<xsl:template match="Albums/album/*">
</xsl:template>


</xsl:stylesheet>

