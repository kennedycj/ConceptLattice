package com.stonearchscientific.common;

import java.util.BitSet;
import com.google.common.base.Objects;
import com.google.common.collect.Range;
/**
 * A concept of a context (G, M, I) is defined to be a pair (A, B) where:<br>
 * - A is a subset of G<br>
 * - B is a subset of M<br>
 * - A' equals B<br>
 * - B' equals A<br>
 * <br>
 * In this context:<br>
 * - G is the set of objects<br>
 * - M is the set of attributes<br>
 * - I is a binary relation between G and M<br>
 * - A is the extent of the concept (each element having type T)<br>
 * - B is the intent of the concept (each element having type U)<br>
 * - A' is the set of all attributes that are common to all objects in A<br>
 * - B' is the set of all objects that have all attributes in B<br>
 * Davey, BA, &amp; Priestley, HA (2002). Introduction to Lattices and Order (2nd ed.). Cambridge University Press<br>
 * @param <T> extent element type<br>
 * @param <U> intent element type<br>
 */
public class Concept<T, U> {
    private T extent;
    private U intent;

    private BitSet bitset(String bitstring) {
        return BitSet.valueOf(new long[]{Long.parseLong(bitstring, 2)});
    }

    private Concept() {
        this.extent = null;
        this.intent = null;
    }

    public Concept(T extent, U intent) {
        this.extent = extent;
        this.intent = intent;
    }

    public static <T, U> Concept<T, U> none(Class<T> clazz) {
        if (clazz == BitSet.class) {
            return new Concept(new BitSet(), null);
        }
        return new Concept(null, null);
    }

    public T extent() {
        return this.extent;
    }

    public U intent() {
        return this.intent;
    }

    public Concept<T, U> intersect(Concept<T, U> that) {
        if (!(that instanceof Concept)) {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
        if(that.intent == null) {
            return that;
        }
        if (this.intent instanceof Range && that.intent instanceof Range) {
            if(this.intent == Range.all() || that.intent == null) {
                return that;
            }
            if(this.intent == null) {
                return new Concept(new BitSet(), null);
            }
            if(that.intent == Range.all()) {
                return new Concept(this.extent, this.intent);
            }
            Range thisIntent = (Range) this.intent;
            Range thatIntent = (Range) that.intent;
            if(thisIntent.isConnected(thatIntent)) {
                // todo: check if this is the correct way to intersect the Concepts with Range as their extent type
                return new Concept(new BitSet(), thisIntent.intersection(thatIntent));
            }
            return new Concept(new BitSet(), null);
        } else if(this.intent instanceof BitSet && that.intent instanceof BitSet) {
            BitSet thisIntent = (BitSet) this.intent;
            BitSet thatIntent = (BitSet) that.intent;
            BitSet meet = (BitSet) thisIntent.clone();
            meet.and(thatIntent);
            return new Concept(new BitSet(), meet);
        } else {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
    }

    public Concept<T, U> union(Concept<T, U> that) {
        if (!(that instanceof Concept)) {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
        if(this.extent instanceof BitSet) {
            BitSet thisExtent = (BitSet) this.extent;
            BitSet thatExtent = (BitSet) that.extent;
            BitSet join = (BitSet) thisExtent.clone();
            thisExtent.or(thatExtent);
        } else {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
        return this;
    }
    /**
     * For concepts (A, B) and (C, D)<br>
     * - (A, B) &lt;= (C, D) if and only if A is a subset of C<br>
     * - By implication, B is a superset of D, and the reverse implication is also true<br>
     * Davey, BA, &amp; Priestley, HA (2002)<br>
     * @param that the concept to compare to<br>
     * @return true if this concept is &lt;= the given concept<br>
     * @see Concept#greaterOrEqual(Concept)
     */
    public boolean lessOrEqual(Concept<T, U> that) {
        if (!(that instanceof Concept)) {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
        if(this.intent == null) {
            return false;
        }
        if(that.intent == null) {
            return true;
        }
        if (this.intent instanceof Range && that.intent instanceof Range) {
            Range intersectIntent = (Range) this.intersect(that).intent;
            Range thatIntent = (Range) that.intent;
            return intersectIntent == (Range) that.intent;
        } else if(this.intent instanceof BitSet && that.intent instanceof BitSet) {
            BitSet thisIntent = (BitSet) this.intent;
            BitSet thatIntent = (BitSet) that.intent;
            BitSet join = (BitSet) thisIntent.clone();
            join.or(thatIntent);
            return join.cardinality() == thisIntent.cardinality();
        } else {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
    }
    /**
     * For concepts (A, B) and (C, D)<br>
     * - (A, B) &gt;= (C, D) if and only if A is a superset of C<br>
     * - By implication, B is a subset of D, and the reverse implication is also true<br>
     * Davey, BA, &amp; Priestley, HA (2002)<br>
     * @param that the concept to compare to<br>
     * @return true if this concept is &lt;= the given concept<br>
     * @see Concept#lessOrEqual(Concept)
     */
    public boolean greaterOrEqual(Concept<T, U> that) {
        if (!(that instanceof Concept)) {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
        if(this.intent == null) {
            return true;
        }
        if(that.intent == null) {
            return false;
        }
        if (this.intent instanceof Range && that.intent instanceof Range) {
            Range intersectIntent = (Range) this.intersect(that).intent;
            Range thatIntent = (Range) that.intent;
            return intersectIntent == (Range) this.intent;
        } else if(this.intent instanceof BitSet && that.intent instanceof BitSet) {
            BitSet thisIntent = (BitSet) this.intent;
            BitSet thatIntent = (BitSet) that.intent;
            BitSet meet = (BitSet) thatIntent.clone();
            meet.and(thisIntent);
            // System.out.println(thisIntent + " and " + thatIntent + " = " + meet);
            return meet.cardinality() == thisIntent.cardinality();
        } else {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
    }

    @Override
    public boolean equals(final Object that) {
        if (!(that instanceof Concept)) {
            return false;
        }
        if (that == this) {
            return true;
        }
        Concept concept = (Concept) that;
        Class<?> clazz = concept.extent.getClass();
        if (this == Concept.none(clazz) && that == Concept.none(clazz)) {
            return true;
        }
        return java.util.Objects.equals(concept.extent, this.extent) && java.util.Objects.equals(concept.intent, this.intent);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.extent);
        if(this.intent == null){
            sb.append("()");
        } else {
            sb.append(this.intent);
        }
        return sb.toString();
    }
}