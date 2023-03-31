import logging

package_logger = logging.getLogger(__name__)
package_logger.addHandler(logging.NullHandler())

