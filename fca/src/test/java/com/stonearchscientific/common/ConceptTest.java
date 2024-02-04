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

        //System.out.println("w = " + w.intent());
        //System.out.println("x = " + x.intent());
        //System.out.println("y = " + y.intent());

        BitSet and = (BitSet) x.intent().clone();
        and.and(w.intent());
        //System.out.println("x & w = " + and);
        //System.out.println("|x & w| = " + and.cardinality());

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
        assertTrue(z.lessOrEqual(x));
        assertFalse(x.lessOrEqual(y));
        assertFalse(y.lessOrEqual(x));
        assertFalse(x.lessOrEqual(z));
    }
    @Test
    public void testRangeLessOrEqual() {
        assertTrue(b.lessOrEqual(b));
        assertTrue(b.lessOrEqual(a));
        assertTrue(d.lessOrEqual(b));
        assertFalse(b.lessOrEqual(c));
        assertFalse(c.lessOrEqual(b));
        assertFalse(b.lessOrEqual(d));
    }
    @Test
    public void testBitSetGreaterOrEqual() {
        assertTrue(x.greaterOrEqual(x));
        assertTrue(w.greaterOrEqual(x));
        assertTrue(x.greaterOrEqual(z));
        assertFalse(x.greaterOrEqual(y));
        assertFalse(y.greaterOrEqual(x));
        assertFalse(z.greaterOrEqual(x));
    }
    @Test
    public void testBitSetIntersect() {
        assertEquals(x.intersect(x).intent(), x.intent());
        assertEquals(x.intersect(w).intent(), w.intent());
        assertEquals(z.intersect(x).intent(), x.intent());
        assertEquals(x.intersect(y).intent(), w.intent());
        assertEquals(y.intersect(x).intent(), w.intent());
        assertEquals(x.intersect(z).intent(), x.intent());
    }
    @Test
    public void testRangeIntersect() {
        assertEquals(b.intersect(b), b);
        assertEquals(b.intersect(c), Concept.none());
        assertEquals(c.intersect(b), Concept.none());
        assertEquals(b.intersect(d), b);
        assertEquals(Concept.none().intersect(Concept.none()), Concept.none());
        assertEquals(b.intersect(Concept.none()), Concept.none());
        assertEquals(d.intersect(b).intent(), b.intent()); // This fails without specifying the intent
        Concept<BitSet, Range<Integer>> p = new Concept<>(bitset("11010"), Range.closed(3, 5));
        assertEquals(p.intersect(d), b);
    }
    @Test
    public void testEqual() {
        assertTrue(x.equals(x));
        assertTrue(Concept.none().equals(Concept.none()));
        assertFalse(x.equals(Concept.none()));
        assertFalse(x.equals(y));
        assertFalse(x.equals(z));
        assertFalse(x.equals(null));
        assertFalse(x.equals(new Object()));
    }


}