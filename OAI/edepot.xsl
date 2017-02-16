<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:oai="http://www.openarchives.org/OAI/2.0/"
    xmlns:srw_dc="info:srw/schema/1/dc-schema"
    xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
    xmlns:dc="http://purl.org/dc/elements/1.1/">

<xsl:variable name="lcletters">abcdefghijklmnopqrstuvwxyz</xsl:variable>
<xsl:variable name="ucletters">ABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>

<xsl:variable name="oai_setname">EDEPOT</xsl:variable>


<xsl:output method="xml" omit-xml-declaration="yes" standalone="yes" indent="yes"/>

    <xsl:template match="/oai:OAI-PMH">
     <xsl:text disable-output-escaping="yes"> &lt;add&gt;</xsl:text>
        <xsl:apply-templates select="oai:GetRecord"/>
     <xsl:text disable-output-escaping="yes"> &lt;/add&gt;</xsl:text>
    </xsl:template>

    <xsl:template match="oai:GetRecord">
        <xsl:apply-templates select="oai:record"/>
    </xsl:template>

    <xsl:template match="oai:record">
     <xsl:text disable-output-escaping="yes"> &lt;doc&gt;</xsl:text>
        <xsl:apply-templates select="oai:header"/>
        <xsl:apply-templates select="oai:metadata"/>
     <xsl:text disable-output-escaping="yes"> &lt;/doc&gt;</xsl:text>
    </xsl:template>

    <xsl:template match="oai:header/*">
        <xsl:for-each select=".">
          <xsl:variable name="field_name">
          <xsl:choose>
            <xsl:when test="contains(name(.), 'identifier')">
                <xsl:text>id</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="name(.)"/>
            </xsl:otherwise>
          </xsl:choose>
          </xsl:variable>

          <xsl:variable name="field_value" select="."/>

          <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
          <xsl:value-of select="$field_name"/>
          <xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
          <xsl:value-of select="$field_value"/>
          <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>

          <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
          <xsl:value-of select="$field_name"/>_str<xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
          <xsl:value-of select="$field_value"/>
          <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
        </xsl:for-each>

        <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>oai_setname_str<xsl:text disable-output-escaping="yes">"&gt;</xsl:text><xsl:value-of select="$oai_setname"/><xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
    </xsl:template>

    <xsl:template match="oai:metadata/*">
        <xsl:for-each select="*">
            <xsl:variable name="field_name">
                <xsl:choose>
                 <xsl:when test="contains(name(.), ':')">
                    <xsl:value-of select="translate(substring-after(name(.), ':'), $ucletters, $lcletters)"/>
                 </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="translate(name(.), $ucletters, $lcletters)"/>
                </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>

            <xsl:variable name="field_value" select="."/>

            <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
            <xsl:value-of select="$field_name"/>
            <xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
            <xsl:value-of select="$field_value"/>
            <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>

            <xsl:text disable-output-escaping="yes">&lt;field name="</xsl:text>
            <xsl:value-of select="$field_name"/><xsl:text>_str</xsl:text>
            <xsl:text disable-output-escaping="yes">"&gt;</xsl:text>
            <xsl:value-of select="$field_value"/>
            <xsl:text disable-output-escaping="yes">&lt;/field&gt;</xsl:text>
        </xsl:for-each>
    </xsl:template>

</xsl:stylesheet>
