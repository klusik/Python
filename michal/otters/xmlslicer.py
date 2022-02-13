#!/usr/bin/env python
#
# xmlslicer.py
#   - Slices the input XML EXAM result data report file into multiple smaller
#   XML files, adding Nekeda metadata as needed. The slicing is done on entire
#   groups, i.e. groups are put to individual files with the same "header" (all
#   the XML content except the <resultData/> content.
#


# import required modules {{{
import argparse
import logging
import os
import sys
import xml.etree.ElementTree
# }}}


logger = logging.getLogger(__name__)

# class XMLSlicer() {{{
class XMLSlicer(object):
    # DOC {{{
    """Slices the input XML EXAM result data report file into multiple smaller
    XML files, adding Nekeda metadata as needed. The slicing is done on entire
    groups, i.e. groups are put to individual files with the same "header" (all
    the XML content except the <resultData/> content.

    The expected format of the input XML file is roughly:

               /                   <?xml ... ?>
               |                   <examResultData ...>
               |                   ...
      "header" |             /     <metaData category="..." ...>
               |    metadata |     ... metadata here
               |             \     </metadata>
               |                   ... metadata or romething else
               \                   <resultData>

                             /     <grp...>
                             |     ... test results and sub groups
              this is sliced |     </grp>
                             |
                             \     ... more groups

                /                  </resultData>
       "header" |                  ...
                \                  </examResultData>


    Other than the slicing, some metadata for the Nekeda tool are inserted if
    missing. The Nekeda metadata are considered missing if the first
    <metaData/> does not have an empty catagery (category=""). The Nekeda
    metadata are read from the specified "XML-like" .txt file, that is missing
    the XML docstring <?xml ...?> and a root node. I.e. something like this:

        <fileType id="examResultDataFile" protected="no" version="2.0"/>
        <metaData category="" export="true">
        <metaDataItem label="project" value="PR-HYB-0-Projektuebergreifend"/>
        <metaDataItem label="mail" value=""/>
        ...
        <metaDataItem label="TestEnvironment" value="HiL"/>
        <metaDataItem label="Variant" value="BM12"/>
        <metaDataItem label="Tester" value="Skala, Petr"/>
        </metaData>


    The <fileType .../> tag is ignored and the first <metaData.../> is inserted
    to all sliced XMLs where it is expected by Nekeda, i.e. as the first
    <metaData.../> in the XML file.
    """
    # }}}

    # STATIC VARIABLES {{{
    # the current version of the slicer
    NAME_AND_VERSION = f"XMLSlicer 1.0"

    # the default maximum size of each sliced output XML file
    DEFAULT_MAX_SIZE_MB = 20

    # the default format (str.format()) of the name of the output XML file
    DEFAULT_OUTPUT_FILE_NAME_FORMAT = "{noExtInputXMLFileName}_part_{partNumber:02d}.xml"

    # the default encoding of the output XML files
    DEFAULT_ENCODING    = "utf-8"

    # the <metaData/> tag name
    TAG_METADATA = "metaData"

    # the category= attribute of the <metaData/> tag
    ATTR_METADATA_CATEGORY = "category"

    # the <resultData/> tag name
    TAG_RESULTDATA = "resultData"

    # the wrapper format (str.format()) that makes the specified Nekeda .txt
    # file a full fledged XML
    NEKEDA_DATA_WRAPPER_FORMAT = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' +
        "<root>\n" +
        "{}\n" +
        "</root>"
    )
    # }}}

    # METHODS {{{
    def __init__(self, inputXMLFileName, nekedaDataFileName = None,
            maxSizeMB = DEFAULT_MAX_SIZE_MB,
            outputFileNamesFormat = DEFAULT_OUTPUT_FILE_NAME_FORMAT,
            outputFilesEncoding = DEFAULT_ENCODING, debug = False,
        ):
        # DOC {{{
        """Initialize instance, store parameters, setup logging, prepare
        placeholders.

        Parameters

            inputXMLFileName -- the name / path of the input XML file

            nekedaDataFileName -- (optional) the name / path of the txt file
                with nekeda data

            maxSizeMB -- (optional) the maximum size of each part (in MB)

            outputFileNamesFormat -- (optional) the format of the output file
                names

            outputFilesEncoding -- (optional) the encoding of the output files

            debug -- (optional) turn debugging on (more logging)
        """
        # }}}

        # CODE {{{

        # make sure that the input exists
        assert (os.path.exists(inputXMLFileName))

        # set the logger level
        logger.setLevel(logging.DEBUG if (debug) else logging.INFO)

        # store parameters {{{
        # the name / path of the input file
        self.inputXMLFileName       = inputXMLFileName

        logger.info(f"inputXMLFileName={inputXMLFileName}")

        # the txt file with the nekeda data
        self.nekedaDataFileName     = nekedaDataFileName

        logger.info(f"nekedaDataFileName={nekedaDataFileName}")

        # determine the maximum size of a part in bytes
        self.maxSize                = (1024*1024) * maxSizeMB

        logger.info(f"maxSize={self.maxSize}")

        # the format of the output file
        self.outputFileNamesFormat   = outputFileNamesFormat

        logger.info(f"outputFileNamesFormat={outputFileNamesFormat}")

        # the encoding of the output files
        self.outputFilesEncoding    = outputFilesEncoding

        logger.info(f"outputFilesEncoding={outputFilesEncoding}")
        # }}}

        # the name of the input XML file without extension
        self.noExtInputXMLFileName = os.path.splitext(inputXMLFileName)[0]

        logger.debug(f"noExtInputXMLFileName={self.noExtInputXMLFileName}")

        # placeholders for internal stuff {{{
        self._xmlReportTree     = None
        self._rootElement       = None
        self._resultDataElement = None
        self._groupElements     = None
        self._headerSize        = None
        self._groupSizes        = None
        # }}}
        # }}}


    @staticmethod
    def fromArguments(argv = None):
        # DOC {{{
        """Creates a new instance of XMLSlicer() from the specified parameters
        (as argv) or from command line arguments (if argv is None).
        """
        # }}}

        # CODE {{{
        parser = argparse.ArgumentParser(
            description     = "slices the input XML file to multiple files",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(
            metavar = "inputXML",
            dest    = "inputXMLFileName",
            help    = "the name / path of the input XML file",
        )

        parser.add_argument(
            "-n", "--nekeda-data",
            dest        = "nekedaDataFileName",
            help        = "the name / path of the txt file with nekeda data",
        )

        parser.add_argument(
            "-s", "--size",
            dest    = "maxSizeMB",
            help    = "the maximum size of each part (in MB)",
            type    = int,
            default = XMLSlicer.DEFAULT_MAX_SIZE_MB,
        )

        parser.add_argument(
            "-f", "--format",
            dest    = "outputFileNamesFormat",
            help    = "the format of the output file names",
            default = XMLSlicer.DEFAULT_OUTPUT_FILE_NAME_FORMAT,
        )

        parser.add_argument(
            "-e", "--encoding",
            dest    = "outputFilesEncoding",
            help    = "the encoding of the output files",
            default = XMLSlicer.DEFAULT_ENCODING,
        )

        parser.add_argument(
            "-d", "--debug",
            dest    = "debug",
            help    = "turn debugging on (more logging)",
            action  = "store_true",
        )

        parser.add_argument(
            "-v", "--version",
            action  = "version",
            version = XMLSlicer.NAME_AND_VERSION,
        )

        parameters = vars(parser.parse_args(argv))

        return XMLSlicer(**parameters)
        # }}}


    def go(self):
        # DOC {{{
        """Does the slicing.
        """
        # }}}

        # CODE {{{
        logger.info(self.NAME_AND_VERSION)

        # read the entire XML
        self._xmlReportTree = xml.etree.ElementTree.parse(self.inputXMLFileName)

        # get the root of the tree
        # NOTE: root is <examResultData/>
        self._rootElement = self._xmlReportTree.getroot()

        logger.debug(f"Root element name: {self._rootElement.tag}")

        # find the <resultData/> element
        self._resultDataElement = self._rootElement.find(self.TAG_RESULTDATA)

        # read and add the <metaData ...> for Nekeda
        self._addNekedaMetadata()

        # dissect (get and remove) the individual groups <grp/> from the <resultData/>
        self._dissectResultData()

        # calculate the size of the header (leftover XML tree) and of each group <grp/>
        self._calcSizes()

        # initialize the first sliced part
        # NOTE: represents just some meta info about the part, not the actual data
        currentPart = SlicedXMLPart(
            partNumber  = 1,
            headerSize  = self._headerSize,
        )

        for groupNumber, (groupSize, groupElement) in enumerate(zip(self._groupSizes, self._groupElements)):
            # write the part, reset the tree and start the next part if adding
            # this group would make the result XML too big
            # NOTE: empties the <resultData/>
            if (currentPart.size + groupSize > self.maxSize):
                currentPart = self._writePartAndStartNext(currentPart)

            logger.debug(
                f"Adding group {groupNumber}:{groupElement.get('name')}."
            )

            # add the group to the current part (metadata about it)
            currentPart.addGroup(groupElement, groupSize)

            # add the group to the result element (the actual element to the XML tree)
            self._resultDataElement.append(groupElement)

        # write the last part of remaining groups
        self._writePartAndStartNext(currentPart)
        # }}}


    def _addNekedaMetadata(self):
        # DOC {{{
        """Adds the nekeda metadata to the XML tree from the associated nekeda
        data file (if necessary).
        """
        # }}}

        # CODE {{{
        insertIndex = None

        # look for the <metaData/> before which to insert the nekeda metadata
        for index, child in enumerate(self._rootElement):
            if (child.tag == self.TAG_METADATA):
                if (child.get(self.ATTR_METADATA_CATEGORY).strip()):
                    insertIndex = index
                    logger.debug(f"Found a location where to place nekeda metadata: _rootElement[{index}].")
                    break
                # return if the Nekeda <metadata/> seems present
                else:
                    logger.debug(f"Nekeda metadata are already present, nothing to insert.")
                    return

        # return if no metadata was found
        if (insertIndex is None):
            raise Exception(
                f"No <metaData/> found in {self.inputXMLFileName}!"
            )

        if (self.nekedaDataFileName is None):
            raise Exception(
                "No Nekeda data file (name) was provided, yet the input xml " +
                "does not have the Nekeda metadata!"
            )

        # read the XML-like metadata as plaintext (because there is no root node)
        with open(self.nekedaDataFileName, "r") as nekedaDataFile:
            nekedaData = nekedaDataFile.read()

        logger.debug(f"Nekeda metadata from {self.nekedaDataFileName}:\n{nekedaData}")

        # wrap the plaintext nekeda metadata in simple XML node
        wrappedNekedaData = self.NEKEDA_DATA_WRAPPER_FORMAT.format(nekedaData)

        logger.debug(f"Wrapped Nekeda metadata:\n{wrappedNekedaData}")

        # parse the nekeda metadata wrapped XML
        nekedaDataRoot = xml.etree.ElementTree.fromstring(wrappedNekedaData)

        # look for the metadata element
        for child in nekedaDataRoot:
            if (child.tag == self.TAG_METADATA):
                nekedaMetadataElement = child
                break
        # raise an exception if the (nekeda) metadata was not found
        else:
            raise Exception(
                f"No <metaData/> found in {self.nekedaDataFileName}!"
            )

        # insert the nekeda metadata to the xml report tree
        self._rootElement.insert(insertIndex, nekedaMetadataElement)
        # }}}


    def _dissectResultData(self):
        # DOC {{{
        """Dissects (gets and removes) the individual groups <grp/> from the
        <resultData/>.
        """
        # }}}

        # CODE {{{
        # get all groups <grp/> from the <resultData/>
        self._groupElements = list(self._resultDataElement)

        logger.info(f"Found {len(self._groupElements)} (top) groups.")

        # remove all groups, so what is left is a bare "header" tree
        for groupElement in reversed(self._groupElements):
            self._resultDataElement.remove(groupElement)
        # }}}


    def _calcSizes(self):
        # DOC {{{
        """Calculate sizes (in bytes) of the "header" (the bare XML tree) and
        each group <grp/>.
        """
        # }}}

        # CODE {{{
        self._headerSize = len(xml.etree.ElementTree.tostring(self._rootElement))

        logger.info(f"Approximate header size: {self._headerSize}")

        self._groupSizes = [
            len(xml.etree.ElementTree.tostring(groupElement))
            for groupElement in self._groupElements
        ]

        logger.info(
            f"Approximate total size of all groups: {sum(self._groupSizes)}"
        )
        # }}}


    def _writePartAndStartNext(self, part):
        # DOC {{{
        """Writes the part, reset the tree and create and return the next part
        if adding this group would make the result XML too big.
        """
        # }}}

        # CODE {{{
        if (part.groupElements):
            outputFileName = self.outputFileNamesFormat.format(
                noExtInputXMLFileName   = self.noExtInputXMLFileName,
                partNumber              = part.number,
            )

            logger.info(
                f"Writting part {part.number} to '{outputFileName}' " +
                f"({len(part.groupElements)} groups, totalSize {part.size})."
            )

            self._xmlReportTree.write(
                file_or_filename    = outputFileName,
                encoding            = self.outputFilesEncoding,
                xml_declaration     = True,
            )

            # remove all added groups from the <resultData/> element
            for partGroupElement in reversed(part.groupElements):
                self._resultDataElement.remove(partGroupElement)

        # create and return the next part
        return part.next()
        # }}}


    # }}}
# }}}


# class SlicedXMLPart() {{{
class SlicedXMLPart(object):
    # DOC {{{
    """Represents just some meta info about the sliced part, not the actual
    data.
    """
    # }}}

    # METHODS {{{
    def __init__(self, partNumber, headerSize):
        # DOC {{{
        """Initializes instance, stores parameters.
        """
        # }}}

        # CODE {{{
        # the number of the part
        self.number     = partNumber

        # the size of the header
        self.headerSize = headerSize

        # the current size of a part in bytes (start with just a header)
        self.size       = headerSize

        # the groups added to the part
        self.groupElements     = []
        # }}}


    def addGroup(self, groupElement, groupSize):
        # DOC {{{
        """Adds the specified group to the part (basically just registers it).
        """
        # }}}

        # CODE {{{
        self.groupElements.append(groupElement)
        self.size += groupSize
        # }}}


    def next(self):
        # DOC {{{
        """Returns a new instance of a part having the next number and the same
        header size.
        """
        # }}}

        # CODE {{{
        return SlicedXMLPart(
            partNumber  = self.number + 1,
            headerSize  = self.headerSize,
        )
        # }}}


    # }}}
# }}}


def main(argv = None):
    # DOC {{{
    """
    """
    # }}}

    # CODE {{{
    XMLSlicer.fromArguments(argv).go()
    # }}}


if (__name__ == "__main__"):
    logging.basicConfig(level=logging.DEBUG)
    main()
