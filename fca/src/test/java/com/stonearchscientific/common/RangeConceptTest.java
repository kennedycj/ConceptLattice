package com.stonearchscientific.common;

import java.util.BitSet;
import com.google.common.collect.Range;
import static org.junit.Assert.fail;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;

import org.junit.Before;
import org.junit.Test;

public final class RangeConceptTest {
    private Concept<BitSet, Range<Integer>> a, b, c, d;

    private BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
    }

    @Before
    public void setUp() {
        a = new Concept<>(bitset("11111"), null);
        b = new Concept<>(bitset("11010"), Range.closed(3, 4));
        c = new Concept<>(bitset("11101"), Range.closed(1, 2));
        d = new Concept<>(bitset("11000"), Range.closed(0, 4));
    }
    @Test
    public void testLessOrEqual() {
        assertTrue(b.lessOrEqual(b));
        assertTrue(b.lessOrEqual(a));
        assertTrue(d.lessOrEqual(b));
        assertFalse(b.lessOrEqual(c));
        assertFalse(c.lessOrEqual(b));
        assertFalse(b.lessOrEqual(d));
    }
    @Test
    public void testGreaterOrEqual() {
        Concept<BitSet, Range<Integer>> ALL = new Concept<>(bitset("11010"), Range.all());
        assertTrue(ALL.greaterOrEqual(ALL));
        assertTrue(a.greaterOrEqual(ALL));
        assertTrue(b.greaterOrEqual(ALL));
        assertTrue(b.greaterOrEqual(d));
        assertFalse(ALL.greaterOrEqual(a));
        assertFalse(ALL.greaterOrEqual(b));
        assertFalse(b.greaterOrEqual(c));
        assertFalse(c.greaterOrEqual(b));
        assertFalse(d.greaterOrEqual(b));
    }
    @Test
    public void testIntersect() {
        assertEquals(b.intersect(b).intent(), b.intent());
        assertEquals(b.intersect(c), Concept.none(BitSet.class));
        assertEquals(c.intersect(b), Concept.none(BitSet.class));
        assertEquals(b.intersect(d).intent(), b.intent());
        assertEquals(Concept.none(BitSet.class).intersect(Concept.none(BitSet.class)), Concept.none(BitSet.class));
        assertEquals(b.intersect(Concept.none(BitSet.class)), Concept.none(BitSet.class));
        assertEquals(d.intersect(b).intent(), b.intent()); // This fails without specifying the intent
        Concept<BitSet, Range<Integer>> p = new Concept<>(bitset("11010"), Range.closed(3, 5));
        assertEquals(p.intersect(d).intent(), b.intent());
    }
    @Test
    public void testEqual() {
        assertTrue(a.equals(a));
    }


}