#!/usr/bin/awk -f
BEGIN{FS="\t"}
{
        max=max<NF?NF:max
        for(i=1;i<=NF;i++) a[NR,i]=$i
}
END{
        i=1; j=1; printf ((j,i) in a)?a[j,i]:""
        for(j=2;j<=NR;j++) printf ((j,i) in a)?"\t"a[j,i]:"\t"
        for(i=2;i<=max;i++) {
                printf "\n"
                j=1; printf ((j,i) in a)?a[j,i]:""
                for(j=2;j<=NR;j++) printf ((j,i) in a)?"\t"a[j,i]:"\t"
        }
}

