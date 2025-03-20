xquery version "1.0";

import module namespace xdb="http://exist-db.org/xquery/xmldb";
import module namespace gen="http://teipublisher.com/generate" at "post-install-generate.xql";

(: The following external variables are set by the repo:deploy function :)

(: file path pointing to the exist installation directory :)
declare variable $home external;
(: path to the directory containing the unpacked .xar package :)
declare variable $dir external;
(: the target collection into which the app is deployed :)
declare variable $target external;

(: To speed up indexing, we pre-calculate some of the data into generated XML files :)
gen:generate-all($target),

(: In the original code from Jinntec, the `xdb:store-files-from-pattern` function was executed in the pre-install.xql
file. We encountered issues with index creation, such as sent-count and received-count being zero for all persons. It
seems that with the original code, ExistDB indexes each file individually during the package installation, and the order
is dependent on the underlying file system. In our case, the index or register files were loaded into the database before
the letters, which meant that when indexing sent-count and received-count, no letters were present in the database yet.

By moving this operation to post-install.xql, the files are copied into ExistDB without building the index initially.
This allows us to index the two folders separately in the correct order afterward. :)

(: store index configuration files :)
xdb:store-files-from-pattern(concat("/system/config", $target), $dir, "*.xconf"),
xdb:reindex(concat($target, '/data/letters')),
xdb:reindex(concat($target, '/data/index')),
xdb:reindex(concat($target, '/data/generated'))