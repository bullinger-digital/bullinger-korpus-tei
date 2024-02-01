xquery version "3.1";

module namespace idx="http://teipublisher.com/index";

declare namespace tei="http://www.tei-c.org/ns/1.0";
declare namespace dbk="http://docbook.org/ns/docbook";

declare variable $idx:app-root :=
    let $rawPath := system:get-module-load-path()
    return
        (: strip the xmldb: part :)
        if (starts-with($rawPath, "xmldb:exist://")) then
            if (starts-with($rawPath, "xmldb:exist://embedded-eXist-server")) then
                substring($rawPath, 36)
            else
                substring($rawPath, 15)
        else
            $rawPath
    ;

(:~
 : Helper function called from collection.xconf to create index fields and facets.
 : This module needs to be loaded before collection.xconf starts indexing documents
 : and therefore should reside in the root of the app.
 :)
declare function idx:get-metadata($root as element(), $field as xs:string) {
    let $header := $root/tei:teiHeader
    return
        switch ($field)
            case "title" return
                $header//tei:titleStmt/tei:title
            case "number" return
                $header//tei:seriesStmt/tei:title[@subtype='publication']
            case "sender" return (
                $header//tei:correspDesc/tei:correspAction[@type="sent"]/tei:persName/@ref/string()
            )
            case "correspondant" return (
                $header//tei:correspDesc/tei:correspAction/tei:persName/@ref/string()
            )
            case "recipient" return (
                $header//tei:correspDesc/tei:correspAction[@type="received"]/tei:persName/@ref/string()
            )
            case "archive" return
                $header//tei:msDesc/tei:msIdentifier/tei:repository/@ref/string()
            case "group" return (
                $header//tei:correspDesc/tei:correspAction/tei:roleName/@ref/string()
            )
            case "institution" return (
                $header//tei:correspDesc/tei:correspAction/tei:orgName/@ref/string()
            )
            case "person-name" return (
                string-join(($root/tei:persName[@type="main"]/tei:surname, $root/tei:persName[@type="main"]/tei:forename),", ")
            )
            case "place-name" return (
                let $settlement := $root//tei:settlement/text()
                let $district := $root//tei:district/text()
                let $country := $root//tei:country/text()
                return
                    if($settlement) then ($settlement) else if ($district) then ($district) else ($country)
            )
            case "place" return (
                $header//tei:correspDesc/tei:correspAction/tei:placeName/@source/string()
            )
            case "language" return
                $header/tei:langUsage/tei:language
            case "date" 
            case "datestring" return            
                let $date := $header//tei:correspAction[@type='sent']/tei:date
                return 
                    head(($date/@when, $date/@notAfter))
            case "archive-name" return
                string-join(($root/tei:orgName/text(), $root/tei:addName/text()), ", ")
            case "archive-count" return
                let $id := $root/@xml:id
                let $letters := collection('/db/apps/bullinger-data/data/letters')//tei:TEI[.//tei:repository/@ref=$id]
                let $count := if($letters)
                            then ( count($letters)) 
                            else 0
                return
                    $count
            case "org-name-sing" return
                $root/tei:name[@xml:lang="de"][@type="sg"]
            case "org-name-plur" return
                $root/tei:name[@xml:lang="de"][@type="pl"]
            case "org-sent-count" return
                let $id := $root/@xml:id
                let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[.//tei:correspAction[@type="sent"]/tei:orgName/@ref=$id]
                let $count := if($letters)
                            then ( count($letters)) 
                            else 0
                return
                    $count
            case "org-received-count" return
                let $id := $root/@xml:id
                let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[.//tei:correspAction[@type="received"]/tei:orgName/@ref=$id]
                let $count := if($letters)
                            then ( count($letters)) 
                            else 0
                return
                    $count
            case "group-name-sing" return
                $root/tei:form[@xml:lang="de"][@type="sg"]
            case "group-name-plur" return
                $root/tei:form[@xml:lang="de"][@type="pl"]
            case "group-sent-count" return
                let $id := $root/@xml:id
                let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[.//tei:correspAction[@type="sent"]/tei:roleName/@ref=$id]
                let $count := if($letters)
                            then ( count($letters)) 
                            else 0
                return
                    $count
            case "group-received-count" return
                let $id := $root/@xml:id
                let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[.//tei:correspAction[@type="received"]/tei:roleName/@ref=$id]
                let $count := if($letters)
                            then ( count($letters)) 
                            else 0
                return
                    $count
            case "group-total-count" return
                let $id := $root/@xml:id
                let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[.//tei:roleName/@ref=$id]
                let $count := if($letters)
                            then ( count($letters)) 
                            else 0
                return
                    $count

            default return
                ()
};