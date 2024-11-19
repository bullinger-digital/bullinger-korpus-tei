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
            case "hbbw-number" return
                if(starts-with($root/@source/string(), "HBBW-")) then
                    ($root/@n/string())
                else
                    ()
            case "letter-id" return
                replace($root/@xml:id/string(), 'file', '')
            case "signature" return
                $root//tei:sourceDesc/tei:msDesc/tei:msIdentifier/tei:idno[@subtype='Autograph' or @subtype='Kopie']
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
            case "organization" return (
                $header//tei:correspDesc/tei:correspAction/tei:orgName/@ref/string()
            )
            case "place-name" return (
                let $settlement := $root//tei:settlement/text()
                let $district := $root//tei:district/text()
                let $country := $root//tei:country/text()
                return
                    if($settlement) then ($settlement) else if ($district) then ($district) else ($country)
            )
            case "place" return (
                $header//tei:correspDesc/tei:correspAction/tei:placeName/@ref/string()
            )
            case "language" return
                $header/tei:langUsage/tei:language
            case "date" 
            case "datestring" return            
                let $date := $header//tei:correspAction[@type='sent']/tei:date
                return 
                    idx:normalize-date(head(($date/@when, $date/@notAfter)))
            default return
                ()
};

declare function idx:normalize-date($date as xs:string) {
    if (matches($date, "^\d{4}-\d{2}$")) then
        xs:date($date || "-01")
    else if (matches($date, "^\d{4}$")) then
        xs:date($date || "-01-01")
    else
        xs:date($date)
};

declare function idx:archive-get-metadata($archive as element(), $field as xs:string) {
    switch ($field)
        case "archive-name" return
                string-join(($archive/tei:orgName/text(), $archive/tei:addName/text()), ", ")
        case "archive-count" return
            let $id := $archive/@xml:id
            let $letters := collection('/db/apps/bullinger-data/data/letters')//tei:TEI[ft:query(.//tei:text, 'archive:' || $id)]
            let $count := if($letters)
                        then ( count($letters)) 
                        else 0
            return
                $count
        default return 
            ()
};


declare function idx:person-get-metadata($person as element(), $field as xs:string) {
    let $main-persname := $person/tei:persName[@type='main']
    let $main-id := fn:lower-case($person/@xml:id)
    
    return switch ($field)
        case "name" return (
            string-join(($main-persname/tei:surname, $main-persname/tei:forename),", ")
        )
        case "surname" return (
            $main-persname/tei:surname
        )
        case "forename" return (
            $main-persname/tei:forename
        )
        case "sent-count" return
            let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[ft:query(.//tei:text, 'sender:' || $main-id)]
            let $count := if($letters)
                        then (count($letters)) 
                        else 0
            return
                $count
        case "received-count" return
            let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[ft:query(.//tei:text, 'recipient:' || $main-id)]
            let $count := if($letters)
                        then (count($letters)) 
                        else 0
            return
                $count
        default return 
            ()
};

declare function idx:org-get-metadata($org as element(), $field as xs:string) {
    let $org-id := fn:lower-case($org/@xml:id)
    
    return switch ($field)
        case "org-name" return (
            string($org)
        )
        case "org-count" return
            let $letters := collection('/db/apps/bullinger-data/data/letters')/tei:TEI[ft:query(.//tei:text, 'organization:' || $org-id)]
            let $count := if($letters)
                        then (count($letters)) 
                        else 0
            return
                $count
        default return 
            ()
};