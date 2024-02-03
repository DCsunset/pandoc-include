<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <xsl:output method="text" version="1.0" indent="yes" />

    <xsl:template  match="/">

        <xsl:for-each select="//doxygen/compounddef/sectiondef[@kind='func']/memberdef[@kind='function']">
            <xsl:value-of select="concat('# ', name/text(), '&#10;&#10;')"/>

            <xsl:value-of select="concat(briefdescription/para/text(), '&#10;&#10;')"/>

            <xsl:for-each select="detaileddescription/para/parameterlist[@kind='param']/parameteritem">
                <xsl:value-of select="concat(' - ', '**', parameternamelist/parametername/text(), '**: ', parameterdescription/para/text(), '&#10;')"/>
                <xsl:value-of select="concat('', '&#10;')"/>
            </xsl:for-each>

            <xsl:if test="detaileddescription/para/simplesect[@kind='return']">
                <xsl:value-of select="concat('> **Returns:** ', detaileddescription/para/simplesect[@kind='return']/para/text(), '&#10;')"/>
            </xsl:if>
            <xsl:if test="not(detaileddescription/para/simplesect[@kind='return'])">
                <xsl:value-of select="concat('> **Returns:** ', 'void', '&#10;')"/>
            </xsl:if>

            <xsl:value-of select="concat('&#10;', '&#10;')"/>
        </xsl:for-each>

    </xsl:template>

</xsl:stylesheet>
