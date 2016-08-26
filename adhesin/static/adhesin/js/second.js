

function myExample() {
    var box = document.getElementById('format');
    var format = box.options[box.selectedIndex].text;
    var sample = "";
    if (format == 'FASTA Sequence'){
        sample = ">Sample:      \nMNQYNSSIPKFIVSVFLIVTGFFSSTIKAQELKLMIKINEAVFYDRITSNKIIGTGHLFNREGKKILISSSLEKIKNTPGAYIIRGQNNSAHKLRIRIGGEDWQPDNSGIGMVSHSDFTNEFNIYFFGNGDIPVDTYLISIYATEIEL"
    } else if (format == 'GenBank Identifier'){
        sample = "194680922"
    } else if (format == 'Uniprot Identifier'){
        sample = "P61853"
    }
    
    document.getElementById('text').value=sample
    return false;
}

/*

*/
