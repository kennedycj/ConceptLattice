package com.stonearchscientific.common;

import java.util.BitSet;
import com.google.common.base.Objects;
import com.google.common.collect.Range;

public class Concept<T, U> {
    private T extent;
    private U intent;

    public Concept(T extent, U intent) {
        this.extent = extent;
        this.intent = intent;
    }

    public T extent() {
        return this.extent;
    }

    public U intent() {
        return this.intent;
    }

    public Concept<T, U> intersect(Concept<T, U> that) {
        // code
        return null;
    }

    public Concept<T, U> union(Concept<T, U> that) {
        // code
        return null;
    }

    public boolean lessOrEqual(Concept<T, U> that) {
        if (!(that instanceof Concept)) {
            throw new IllegalArgumentException("Both intent and extent must be instances of Range for intersection.");
        }
        if(that.intent == null) {
            return true;
        }
        if (this.intent instanceof Range && that.intent instanceof Range) {
            Range thisIntent = (Range) this.intent;
            return thisIntent.encloses((Range) that.intent);
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

    public Concept<T, U> greaterOrEqual(Concept<T, U> that) {
        // code
        return null;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(this.extent).append(this.intent);
        return sb.toString();
    }
}