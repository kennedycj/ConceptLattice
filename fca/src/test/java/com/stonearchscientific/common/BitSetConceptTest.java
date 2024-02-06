package com.stonearchscientific.common;

import java.util.BitSet;
import static org.junit.Assert.fail;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

import org.junit.Before;
import org.junit.Test;

public final class BitSetConceptTest {
    private Concept<BitSet, BitSet> w, x, y, z;

    private BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
    }

    @Before
    public void setUp() {
        w = new Concept<>(bitset("11111"), bitset("00000"));
        x = new Concept<>(bitset("11010"), bitset("00001"));
        y = new Concept<>(bitset("11101"), bitset("00100"));
        z = new Concept<>(bitset("11000"), bitset("11101"));
    }
    @Test
    public void testConstructor() {
        Concept<BitSet, BitSet> p = new Concept<>(new BitSet(5), new BitSet(5));
        assertEquals(p.extent(), bitset("00000"));
        assertEquals(p.intent(), bitset("00000"));
        //Concept<BitSet, BitSet> b = new Concept<BitSet, BitSet>(new BitSet());
        //Concept<BitSet, BitSet> c = new Concept<BitSet, BitSet>(new BitSet(), new BitSet());
    }
    @Test
    public void testLessOrEqual() {
        assertTrue(x.lessOrEqual(x));
        assertTrue(x.lessOrEqual(w));
        assertTrue(z.lessOrEqual(x));
        assertFalse(x.lessOrEqual(y));
        assertFalse(y.lessOrEqual(x));
        assertFalse(x.lessOrEqual(z));
    }
    @Test
    public void testGreaterOrEqual() {
        assertTrue(x.greaterOrEqual(x));
        assertTrue(w.greaterOrEqual(x));
        assertTrue(x.greaterOrEqual(z));
        assertFalse(x.greaterOrEqual(y));
        assertFalse(y.greaterOrEqual(x));
        assertFalse(z.greaterOrEqual(x));
    }
    @Test
    public void testIntersect() {
        assertEquals(x.intersect(x).intent(), x.intent());
        assertEquals(x.intersect(w).intent(), w.intent());
        assertEquals(z.intersect(x).intent(), x.intent());
        assertEquals(x.intersect(y).intent(), w.intent());
        assertEquals(y.intersect(x).intent(), w.intent());
        assertEquals(x.intersect(z).intent(), x.intent());
    }
    @Test
    public void testEqual() {
        assertTrue(x.equals(x));
        assertTrue(Concept.none(BitSet.class).equals(Concept.none(BitSet.class)));
        assertFalse(x.equals(Concept.none(BitSet.class)));
        assertFalse(x.equals(y));
        assertFalse(x.equals(z));
        assertFalse(x.equals(null));
        assertFalse(x.equals(new Object()));
    }


}