import logging

import pytest


import boss.runs.reference as refc


@pytest.mark.parametrize("name, seq, ploidy", [
    ("ch1", "ACGTACGT", 1),
    ("ch1", "ACGTACGTNnWwIi", 1),
    ("ch1", "ACGTACGT", 2),
    ("ch2", "ACgtacGT", 1),
    ("ch3  r", "ACGTACGT", 1),
    ("ch_garbage", "NotaREALSequenceGT", 1),
])
def test_contig(name, seq, ploidy):
    c = refc.Contig(name=name, seq=seq, ploidy=ploidy)
    logging.info(c.name)
    logging.info(c.seq)
    logging.info(c.seq_int)
    assert c.length == len(seq)
    assert c.length == len(c.seq_int)
    assert " " not in c.name
    assert c.coverage.shape == (len(seq), 5)
    assert c.coverage.sum() == 0
    assert c.bucket_switches.shape == ((len(seq) // 20_000) + 1, )
    assert c.initial_scores[0] == c.score0


@pytest.mark.xfail(raises=ValueError)
def test_contig_ploidy():
    c = refc.Contig(name="contig1", seq="ACGT", ploidy=3)
    logging.info(c.name)


@pytest.mark.xfail(raises=AssertionError)
def test_contig_seq():
    c = refc.Contig(name="contig1", seq="Not a REAL Sequence", ploidy=1)
    logging.info(c.name)




@pytest.mark.parametrize("ref, mmi, reject_refs, nsites", [
    ("../data/zymo.fa", None, "", 31012581),
    ("../data/zymo.fa", "../data/zymo.fa.mmi", "", 31012581),
    ("../data/zymo.fa", "../data/zymo.fa.mmi", "NZ_CP041014.1,NZ_VFAE01000004.1,NZ_VFAG01000001.1", 27910526),
])
def test_reference(ref, mmi, reject_refs, nsites):
    r = refc.Reference(ref=ref, mmi=mmi, reject_refs=reject_refs)
    assert len(r.contigs) == 9
    assert r.n_sites == nsites


@pytest.mark.xfail(raises=FileNotFoundError)
def test_reference_notafile():
    _ = refc.Reference(ref="not_a_real_file")


@pytest.mark.xfail(raises=ValueError)
def test_reference_notfasta():
    _ = refc.Reference(ref="../data/ERR3152366_10k.fq")   # TODO trigger that one



@pytest.mark.xfail(raises=FileNotFoundError)
def test_reference_unrealmmi():
    _ = refc.Reference(ref="../data/zymo.fa", mmi="not_a_real_file")


@pytest.fixture
def reference():
    r = refc.Reference(ref="../data/zymo.fa", mmi="../data/zymo.fa.mmi")
    return r


def test_contig_dicts(reference):
    cs = reference.contig_sequences()
    cl = reference.contig_lengths()
    assert isinstance(cs, dict)
    assert isinstance(cl, dict)
    assert len(cs) == 9
    assert len(cl) == 9

