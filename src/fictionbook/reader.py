# -*- coding: utf-8 -*-
import base64
import os
import urllib.request
import urllib.error
from xml.etree.ElementTree import parse

from fictionbook.intermediary_xml_format import IntermediaryXmlFormat


class Fb2Reader:
    """
    FictionBook2 reader
    """

    def __init__(self, file_path: str, images_dir: str, download_images=False):
        """
        :param file_path:
        :param images_dir:
        """
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        if not isinstance(images_dir, str):
            raise TypeError("images_dir must be a string")
        self.file_path = file_path
        self.images_dir = images_dir
        self.root = None
        self.metadata = None
        self.body = None
        self.cover_image = None
        if not os.path.isdir(self.images_dir):
            os.mkdir(self.images_dir)
        self._read(download_images)

    @property
    def cover(self):
        return os.path.join(self.images_dir, self.cover_image) if self.cover_image else None

    @property
    def images(self):
        return [os.path.join(self.images_dir, image) for image in os.listdir(self.images_dir)]

    @property
    def paragraphs(self):
        """
        Collect all paragraphs from the body
        Iterate body recursively and collect all paragraphs
        :return: list of paragraphs
        """
        return [paragraph.text for paragraph in self.body.filter_tag('p')] if self.body else []

    def _read(self, download_images=False):
        tree = parse(self.file_path)
        root = tree.getroot()
        self.root = self._to_intermediary_format(element=root)

        self._extract_metadata()
        self._extract_body()
        self._extract_binary()
        if download_images:
            self._download_images(root)

    def _extract_metadata(self):
        """
        Extract metadata ('description' tag) recursively from the root element
        """
        self.metadata = self.root.filter_tag('description')[0]
        assert self.metadata, "Metadata not found"
        self.cover_image = self._extract_cover()

    def _extract_body(self):
        """
        Extract body recursively from the root element
        """
        self.body = self.root.filter_tag('body')[0]
        assert self.body, "Body not found"

    def _extract_binary(self):
        """
        Extract all <binary> elements from root
        """
        binary_elements = self.root.filter_tag('binary')
        for binary in binary_elements:
            binary_id = binary.attributes.get('id', None)
            binary_content = binary.text
            binary_content_type = binary.attributes.get('content-type', None)
            if binary_id and binary:
                self._save_image(binary_content, binary_content_type, binary_id)

    def _to_intermediary_format(self, element):
        """
        Convert xml.etree.ElementTree.Element to IntermediaryXmlFormat
        :param element: xml.etree.ElementTree.Element pointing to the parent element
        :return: IntermediaryXmlFormat object
        """
        # Clean up tag name from namespace prefix
        tag_name = element.tag.split("}")[1] if '}' in element.tag else element.tag

        # Clean up attribute keys from namespace prefixes
        attributes = {key.split("}")[1] if '}' in key else key: value for key, value in element.attrib.items()}

        text = element.text.strip() if element.text else ""
        children = []
        # Recursively set nested properties
        if len(element) > 0:
            for child in element:
                children.append(self._to_intermediary_format(child))
        return IntermediaryXmlFormat(tag_name, attributes, children, text)

    def _extract_cover(self):
        """
        Find the first coverpage element, extract first image element and get the href attribute
        Trim '#' prefix if present
        """
        coverpage = self.metadata.filter_tag('coverpage')
        if len(coverpage) == 0:
            return None

        cover_images = coverpage[0].filter_tag('image')
        if len(cover_images) == 0:
            return None

        # Get href and trim '#' prefix
        href = cover_images[0].attributes.get('href', None)
        if href and href.startswith('#'):
            href = href[1:]
        return href

    def _download_images(self, root):
        """
        Download images from the book if <image l:href="https..."> tag is used
        and points to URL in the internet
        Note: Images may repeat so we use set() to avoid duplicates
        """
        images = set()
        image_elements = root.findall(".//{http://www.gribuser.ru/xml/fictionbook/2.0}image")
        for image_elem in image_elements:
            href_attr = image_elem.attrib.get("{http://www.w3.org/1999/xlink}href", "")
            if href_attr.startswith("http"):
                images.add(href_attr)
        # download images
        for image_url in images:
            self._download_image(image_url)

    def _download_image(self, image_url):
        try:
            with urllib.request.urlopen(image_url) as response:
                if response.code == 200:
                    image_name = os.path.basename(image_url)
                    image_path = os.path.join(self.images_dir, image_name)

                    with open(image_path, 'wb') as image_file:
                        image_file.write(response.read())
        except urllib.error.URLError as e:
            print(f"Error downloading image from {image_url}: {e}")

    def _save_image(self, image_data, content_type, image_id):
        image_extension = content_type.split("/")[-1]
        image_name, ext = os.path.splitext(image_id)

        if not ext:
            ext = f".{image_extension.lower()}"

        image_path = os.path.abspath(os.path.join(self.images_dir, image_name + ext))

        with open(image_path, 'wb') as image_file:
            image_file.write(base64.b64decode(image_data))

        self.images.append(image_path)
