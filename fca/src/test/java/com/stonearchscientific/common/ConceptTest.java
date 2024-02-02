package com.stonearchscientific.common;

import java.util.BitSet;
import com.google.common.collect.Range;
import static org.junit.Assert.fail;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

import org.junit.Before;
import org.junit.Test;

public final class ConceptTest {
    private Concept<BitSet, BitSet> w, x, y, z;
    private Concept<BitSet, Range<Integer>> a, b, c, d;

    private BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
    }

    @Before
    public void setUp() {
        w = new Concept<>(bitset("11111"), bitset("00000"));
        x = new Concept<>(bitset("11010"), bitset("00001"));
        y = new Concept<>(bitset("11101"), bitset("00100"));
        z = new Concept<>(bitset("11000"), bitset("11101"));

        a = new Concept<>(bitset("11111"), null);
        b = new Concept<>(bitset("11010"), Range.closed(3, 4));
        c = new Concept<>(bitset("11101"), Range.closed(1, 2));
        d = new Concept<>(bitset("11000"), Range.closed(0, 4));
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
    public void testBitSetLessOrEqual() {
        assertTrue(x.lessOrEqual(x));
        assertTrue(x.lessOrEqual(w));
        assertFalse(x.lessOrEqual(y));
        assertFalse(y.lessOrEqual(x));
        assertFalse(x.lessOrEqual(z));
        assertTrue(z.lessOrEqual(x));
    }
    @Test
    public void testRangeLessOrEqual() {
        assertTrue(b.lessOrEqual(b));
        assertTrue(b.lessOrEqual(a));
        assertFalse(b.lessOrEqual(c));
        assertFalse(c.lessOrEqual(b));
        assertFalse(b.lessOrEqual(d));
        assertTrue(d.lessOrEqual(b));
    }


}