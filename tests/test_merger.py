from hashlib import sha256

from pdfmerger.main import merger


def test_main():
    files = ["tests/BlankTest_1.pdf", "tests/BlankTest_2.pdf"]
    verify = "tests/BlankTest_verify.pdf"
    output = "tests/BlankTest_output.pdf"
    assert merger(files, output)

    # Now verfiy hashes
    with open(verify, "rb") as fverify, open(output, "rb") as foutput:
        verify_hash = sha256(fverify.read()).hexdigest()
        output_hash = sha256(foutput.read()).hexdigest()
        assert verify_hash == output_hash

    files = ["tests/BlankTest_1.pdf", "tests/BlankTest_1.pdf"]
    verify = "tests/BlankTest_verify.pdf"
    output = "tests/BlankTest_output.pdf"
    assert merger(files, output)

    # Now verfiy hashes
    with open(verify, "rb") as fverify, open(output, "rb") as foutput:
        verify_hash = sha256(fverify.read()).hexdigest()
        output_hash = sha256(foutput.read()).hexdigest()
        assert verify_hash != output_hash
