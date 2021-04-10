"""
This module was solely developed by Dmitry Figol
https://github.com/dmfigol
"""
from typing import Any, Optional, Union
from xml.dom.minidom import parseString

from lxml import etree


def extract_hostname_from_fqdn(fqdn: str) -> str:
    return fqdn.split(".")[0]


def dict_to_xml(
    data: Any, root: Union[None, str, etree._Element] = None, attr_marker: str = "_"
) -> etree.Element:
    namespaces = data.pop("_namespaces", {})

    def _dict_to_xml(data_: Any, parent: Optional[etree._Element] = None) -> None:
        nonlocal root
        if not isinstance(data_, dict):
            raise ValueError("provided data must be a dictionary")

        for key, value in data_.items():
            if key.startswith(attr_marker):
                # handle keys starting with attr_marker as tag attributes
                attr_name = key.lstrip(attr_marker)
                parent.attrib[attr_name] = value
            else:
                if "+" in key:
                    key, *_namespaces = key.split("+")
                    nsmap = {ns: namespaces[ns] for ns in _namespaces}
                else:
                    nsmap = None
                element = etree.Element(key, nsmap=nsmap)
                if root is None:
                    root = element

                if parent is not None and not isinstance(value, list):
                    parent.append(element)

                if isinstance(value, dict):
                    _dict_to_xml(value, element)
                elif isinstance(value, list):
                    for item in value:
                        list_key = etree.Element(key)
                        parent.append(list_key)
                        _dict_to_xml(item, list_key)
                else:
                    if value is True or value is False:
                        value = str(value).lower()
                    elif value is not None and not isinstance(value, str):
                        value = str(value)

                    element.text = value

    if isinstance(root, str):
        root = etree.Element(root)
    _dict_to_xml(data, root)
    return root


def prettify_xml(xml: Union[str, etree._Element]) -> str:
    if isinstance(xml, etree._Element):
        result = etree.tostring(xml, pretty_print=True).decode("utf-8")
    else:
        result = parseString(xml).toprettyxml()
    return result
