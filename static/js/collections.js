/**
 * Namespaced collectins
 *
 * @since 2013-02-24
 */
define(
    "collections",
    ["collections/systems"],
    function(System, Systems) {
      return {Systems: Systems};
    }
);
