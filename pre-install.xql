xquery version "1.0";

import module namespace xdb="http://exist-db.org/xquery/xmldb";

(: The following external variables are set by the repo:deploy function :)

(: file path pointing to the exist installation directory :)
declare variable $home external;
(: path to the directory containing the unpacked .xar package :)
declare variable $dir external;
(: the target collection into which the app is deployed :)
declare variable $target external;

declare function local:mkcol-recursive($collection, $components) {
    if (exists($components)) then
        let $newColl := concat($collection, "/", $components[1])
        return (
            xdb:create-collection($collection, $components[1]),
            local:mkcol-recursive($newColl, subsequence($components, 2))
        )
    else
        ()
};

(: Helper function to recursively create a collection hierarchy. :)
declare function local:mkcol($collection, $path) {
    local:mkcol-recursive($collection, tokenize($path, "/"))
};

(: store the collection configuration :)
local:mkcol(repo:get-root(), replace($target, "^.*/([^/]+)$", "$1")),
sm:chgrp(xs:anyURI($target), "tei"),
sm:chown(xs:anyURI($target), "bullinger"),
xdb:store-files-from-pattern($target, $dir, 'index.xql'),
local:mkcol("/db/system/config", $target)
(: Moved to post-install.xql :)
(: xdb:store-files-from-pattern(concat("/system/config", $target), $dir, "*.xconf") :)